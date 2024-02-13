<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from "svelte-spa-router"
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    import { writable } from "svelte/store";
    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[], voter:[], content:''}
    let answers = []
    let content = ""
    let error = {detail:[]}

    let page = writable(0)
    let size = 5
    let total_answer = 0
    $: total_page = Math.ceil(total_answer/size)

    let reply_total = 0
    let reply_page = 0
    let reply_size = 5

    let focused = null
    let reply_content = ''

    get_question()
    get_answer_list()
    $: $page, get_answer_list()

    function get_question(){
        fastapi("get", "/api/question/detail/"+question_id, {}, (json)=>{
            question = json
        })
    }

    function get_answer_list(){
        let url = "/api/answer/list/"+question_id
        let params = {
            page: $page,
            size: size
        }
        fastapi("get", url, params,
            (json) => {
                total_answer = json.total
                answers = json.answer_list
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    function post_answer(event){
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        let params = {
            content : content
        }
        fastapi('post', url, params,
            (json) => {
                content = ''
                error = {detail:[]}
                get_question()
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    function delete_question(_question_id){
        if(window.confirm('정말로 삭제하시겠습니까?')){
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params,
                (json) => {
                    push('/')
                },
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

    function delete_answer(answer_id){
        if(window.confirm('정말로 삭제하시겠습니까?')){
            let url = "/api/answer/delete"
            let params = {
                answer_id: answer_id
            }
            fastapi('delete', url, params,
                (json) => {
                    get_question()
                },
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

    function vote_question(_question_id){
        if(window.confirm('정말로 추천하시겠습니까?')){
            let url = "/api/question/vote"
            let params = {
                question_id: _question_id
            }
            fastapi('post', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function vote_answer(_answer_id){
        if(window.confirm('정말로 추천하시겠습니까?')){
            let url = "/api/answer/vote"
            let params = {
                answer_id: _answer_id
            }
            fastapi('post', url, params,
                (json) => {
                    get_answer_list()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function get_reply_list(){
        let url = "/api/reply/list" + question_id
        let params = {
            page: reply_page,
            size: reply_size
        }
        fastapi("get", url, params,
            (json) => {
                replies = json
            },
            (err) => {
                error = err
            }
        )
    }

    function post_reply(event, answer_id){
        event.preventDefault()
        let url="/api/reply/create/"+answer_id
        let params = {
            content: reply_content
        }
        fastapi("post", url, params,
            (json) => {
                get_answer_list()
                reply_content = ''
                focused = null
            },
            (err) => {error=err}
        )
    }

    function vote_reply(reply_id){
        if(window.confirm("정말로 추천하시겠습니까?")){
            let url = "/api/reply/vote"
            let params = {
                reply_id: reply_id
            }
            const success = (json) => {get_answer_list()}
            const failure = (err) => {error = err}
            fastapi("post", url, params, success, failure)
        }
    }

    function update_reply(){
        let url = "/api/reply/update"
    }

    function delete_reply(reply_id){
        if(window.confirm('정말로 삭제하시겠습니까?')){
            let url = "/api/reply/delete"
            let params = {
                reply_id: reply_id
            }
            fastapi('delete', url, params,
                (json) => {
                    push('/')
                },
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

</script>

<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">
                {@html marked.parse(question.content)}
            </div>  
            <div class="d-flex justify-content-end">
                {#if question.modify_date}
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <!-- 추천, 수정, 삭제 -->
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary" on:click={vote_question(question.id)}>
                    추천<span class="badge rounded-pill bg-success">{question.voter.length}</span>
                </button>
                {#if question.user && $username === question.user.username}
                <a use:link href="/question-modify/{question.id}"
                class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary" on:click={() => delete_question(question.id)}>삭제</button>
                {/if}
            </div>
        </div>  
    </div>

    <button class="btn btn-secondary" on:click="{() => {push('/')}}">목록으로</button>
    
    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">
                {@html marked.parse(answer.content)}
            </div>
            <div class="d-flex justify-content-end">
                {#if answer.modify_date}
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{answer.user ? answer.user.username : ""}</div>
                    <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <!-- 추천, 수정, 삭제 -->
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary" on:click={vote_answer(answer.id)}>
                    추천<span class="badge rounded-pill bg-success">{answer.voter.length}</span>
                </button>
                {#if answer.user && $username === answer.user.username}
                <a use:link href="/answer-modify/{answer.id}"
                class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary" on:click={() => delete_answer(answer.id)}>삭제</button>
                {/if}
                <button class="btn btn-sm btn-outline-secondary {$is_login ? '' : 'disabled'}" on:click={() => {
                    reply_content = ''
                    focused = answer.id != focused ? answer.id : null
                }}>답글</button>
                <!-- 답글 -->
                {#if focused === answer.id}
                <form method="post" class="my-3">
                    <div class="mb-3">
                        <textarea rows="1" bind:value={reply_content} 
                        disabled={$is_login ? "" : "disabled"}
                        class="form-control"/>
                    </div>
                    <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click="{(event) => post_reply(event, answer.id)}">        
                </form>
                {/if}
            </div>
        </div>
        <!-- 답글 목록 -->
        {#each answer.replies as reply}
        <div class="card-body mx-4">
            <div class="card-text">
                {@html marked.parse(reply.content)}
            </div>
            <div class="d-flex justify-content-end">
                {#if reply.modify_date}
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(reply.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{reply.user ? reply.user.username : ""}</div>
                    <div>{moment(reply.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <!-- 추천, 수정, 삭제 -->
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary" on:click={()=>vote_reply(reply.id)}>
                    추천<span class="badge rounded-pill bg-success">{reply.voter.length}</span>
                </button>
                {#if reply.user && $username === reply.user.username}
                <a use:link href="/reply-modify/{reply.id}"
                class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary" on:click={()=>delete_reply(reply.id)}>삭제</button>
                {/if}
            </div>
        </div>
        {/each}
    </div>
    {/each}
    <ul class="pagination justify-content-center">
        <!-- 처음 페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
          <button class="page-link" on:click="{() => $page = 0}">처음</button>
        </li>
        <!-- 이전 페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
          <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지 번호 -->
        {#each Array(total_page) as _, loop_page}
            {#if loop_page >= $page-5 && loop_page <= $page+5}
            <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
            </li>
            {/if}
        {/each}
        <!-- 다음 페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
          <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
        <!-- 마지막 페이지-->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
          <button class="page-link" on:click="{() => $page = total_page-1}">마지막</button>
        </li>
    </ul>
    <!-- 답변 등록 -->
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} 
            disabled={$is_login ? "" : "disabled"}
            class="form-control"/>
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click="{post_answer}">        
    </form>
</div>