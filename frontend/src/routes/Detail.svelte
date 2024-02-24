<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from "svelte-spa-router"
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    import { writable } from "svelte/store";
    import Pager from "../components/Pager.svelte";
    import Comment from "../components/Comment.svelte";
    import CommentBox from "../components/CommentBox.svelte";
    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {voter:[], content:''}

    let page_answer = 0
    let size_answer = 5
    let total_answer = 0
    let answers = []

    let error = {detail:[]}

    $: total_page = Math.ceil(total_answer/size_answer)

    init()

    function init(){
        fastapi("get", "/api/question/detail/"+question_id, {},
            (json) => {
                question = json
            },
            (err) => {
                error = err
            }
        )

        fastapi("get", "/api/answer/list/"+question_id, 
            {
                page: page_answer,
                size: size_answer
            },
            (json) => {
                answers = json.answer_list
                total_answer = json.total
            },
            (err) => {error=err}
        )
    }
    function post_answer(content){
        let url = "/api/answer/create/" + question_id
        let params = {
            content : content
        }
        fastapi('post', url, params,
            (json) => {
                init()
            },
            (err_json) => {
                error = err_json
            }
        )
    }
    function post_reply(answer_id, reply_content){
        let url="/api/reply/create/"+answer_id
        let params = {
            content: reply_content
        }
        fastapi("post", url, params,
            (json) => {
                init()
            },
            (err) => {error=err}
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
                    init()
                },
                (json_error) => {
                    error = json_error
                }
            )
        }
    }
    function delete_reply(reply_id){
        if(window.confirm('정말로 삭제하시겠습니까?')){
            let url = "/api/reply/delete"
            let params = {
                reply_id: reply_id
            }
            fastapi('delete', url, params,
                (json) => {
                    init()
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
                    init()
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
                    init()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
    function vote_reply(reply_id){
        if(window.confirm("정말로 추천하시겠습니까?")){
            let url = "/api/reply/vote"
            let params = {
                reply_id: reply_id
            }
            const success = (json) => {init()}
            const failure = (err) => {error = err}
            fastapi("post", url, params, success, failure)
        }
    }

</script>

<div class="container my-3">
    <!-- 에러 컴포넌트-->
    <Error error={error}/>

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

    <!-- 목록으로 되돌아가기 버튼 -->
    <button class="btn btn-secondary" on:click="{() => {push('/')}}">목록으로</button>
    
    <!-- 댓글 목록 -->
    <h5 class="border-bottom my-3 py-2">{total_answer}개의 답변이 있습니다.</h5>
    {#each answers as answer}
    <div>
        <Comment
            login_id={$username}
            username={answer.user?.username}
            content={answer.content}
            created_date={moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
            modified_date={moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}
            recommend_count={answer.voter.length}
            on_recommended={() => vote_answer(answer.id)}
            on_modified={() => push('/answer-modify/'+answer.id)}
            on_deleted={() => delete_answer(answer.id)}
            on_replied={(reply_content) => post_reply(answer.id, reply_content)}
        />
        <!--대댓글 목록-->
        <div class="mx-3 my-1">
            {#each answer.replies as reply}
            <Comment 
                login_id={$username}
                username={reply.user?.username}
                content={reply.content}
                created_date={moment(reply.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                modified_date={moment(reply.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}
                recommend_count={reply.voter.length}
                on_recommended={() => vote_reply(reply.id)}
                on_modified={() => push('/reply-modify/'+reply.id)}
                on_deleted={() => delete_reply(reply.id)}
                on_replied={(reply_content) => post_reply(answer.id, reply_content)}
            />
            {/each}
        </div>
    </div>
    {/each}

    <Pager 
        page={page_answer} 
        total_page={total_page}
        on_changed={(page) => {
            page_answer = page
            init()
        }}
    />

    <CommentBox 
        rows={5}
        is_login={$is_login}
        on_submitted={(content) => post_answer(content)}
    />
</div>