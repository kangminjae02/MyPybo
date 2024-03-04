<script>
    import Error from "../components/Error.svelte";
    import fastapi from "../lib/api";

    let error = ''

    let email = ''

    function send_password_reset_email(){
        fastapi("post", "/api/email/password-reset", {email:email},
            (json) => {
                console.log(json)
            },
            (err) => {error = err}
        )
    }

</script>
<Error {error}/>
<div class="position-static">
    <div class="mb-3 position-absolute top-50 start-50 translate-middle">
        <label for="exampleFormControlInput1" class="form-label">이메일을 입력하세요</label>
        <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com" bind:value={email}>
        <button class="btn btn-primary" on:click={() => {send_password_reset_email()}}>전송</button>
    </div>
    
</div>
