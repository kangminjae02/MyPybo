<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from "svelte-spa-router"
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    import { writable } from "svelte/store";
    import Answer from "../components/_Answer.svelte"
    import Pager from "../components/_Pager.svelte"
    import Reply from "../components/_Reply.svelte";
    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[], voter:[], content:''}

    let content = ""
    let error = {detail:[]}

    const answerVM = {
        answers : [],
        page : writable(0),
        size : 5,
        total : 0,
        total_page : 0,
        post : (event) => {
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
        },
        modify : (answer_id) => {
            push('/answer-modify/' + answer_id)
        },
        delete : (answer_id) => {
            if(window.confirm('정말로 삭제하시겠습니까?')){
                let url = "/api/answer/delete"
                let params = {
                    answer_id: answer_id
                }
                fastapi('delete', url, params,
                    (json) => {
                        get_question()
                    },
                    (err) => {
                        error = err
                    }
                )
            }
        },
        vote : (answer_id) => {
            if(window.confirm('정말로 추천하시겠습니까?')){
                let url = "/api/answer/vote"
                let params = {
                    answer_id: answer_id
                }
                fastapi('post', url, params,
                    (json) => {
                        get_answer_list()
                    },
                    (err) => {
                        error = err
                    }
                )
            }
        }
    }

    const replyVM = {
        page : writable(0),
        size : 5,
        total : 0,
        total_page : 0,
        post : (event) => {
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
        },
        modify : (reply_id) => {
            push('/reply-modify/'+reply_id)
        },
        delete : (reply_id) => {
            if(window.confirm('정말로 삭제하시겠습니까?')){
                let url = "/api/reply/delete"
                let params = {
                    reply_id: reply_id
                }
                fastapi('delete', url, params,
                    (json) => {push('/')},
                    (err) => {error = err}
                )
            }
        },
        vote : (reply_id) => {
            if(window.confirm("정말로 추천하시겠습니까?")){
                let url = "/api/reply/vote"
                let params = {
                    reply_id: reply_id
                }
                fastapi("post", url, params, 
                    (json) => {get_answer_list()}, 
                    (err) => {error = err}
                )
            }
        }
    }
    console.log(answerVM.$page)
    get_question()
    get_answer_list()
    $: answerVM.total_page = Math.ceil(answerVM.total/answerVM.size)
    $: replyVM.total_page = Math.ceil(replyVM.total/replyVM.size)
    $: answerVM.$page, console.log(answerVM.$page)
    $: get_answer_list()

    function get_question(){
        fastapi("get", "/api/question/detail/"+question_id, {}, (json)=>{
            question = json
        })
    }

    function get_answer_list(){
        let url = "/api/answer/list/"+question_id
        let params = {
            page: answerVM.$page,
            size: answerVM.size
        }
        fastapi("get", url, params,
            (json) => {
                answerVM.total = json.total
                answerVM.answers = json.answer_list
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

    function get_reply_list(){
        let url = "/api/reply/list" + question_id
        let params = {
            page: replyVM.$page,
            size: replyVM.size
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
    <div>
        {#each answerVM.answers as answer}
        <Answer {answer}/>
            {#each answer.replies as reply}
            <Reply {reply}/>
            {/each}
        {/each}
    </div>
    
    <!-- 페이저 -->
    <Pager props={
        {
            now_page : answerVM.$page,
            total_page : answerVM.total_page,
            begin : () => {answerVM.$page = 0},
            prev : () => {answerVM.$page--},
            move : (loop_page) => {answerVM.$page = loop_page},
            next : () => {answerVM.$page++},
            end : () => {answerVM.$page = answerVM.total_page-1}
        }
    }/>
    
    <!-- 답변 등록 -->
    <Error {error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} 
            disabled={$is_login ? "" : "disabled"}
            class="form-control"/>
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click="{answerVM.post}">        
    </form>
</div>