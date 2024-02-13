<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { push } from "svelte-spa-router"

    export let params = {}
    const reply_id = params.reply_id

    let error = {detail:[]}
    let answer_id = null
    let content = ''

    fastapi("get", "/api/reply/detail/" + reply_id, {}, (json) => {
        answer_id = json.answer_id
        content = json.content
    })

    function update_reply(event){
        event.preventDefault()
        let url = "/api/reply/update"
        let params = {
            reply_id : reply_id,
            content : content
        }
        fastapi('put', url, params,
            (json) => {
                fastapi("get", "/api/answer/detail/"+ answer_id, {}, (json) => {
                    push('/detail/' + json.question_id)
                })
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">답글 수정</h5>
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows=10 bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click = {update_reply}>수정하기</button>
    </form>
</div>