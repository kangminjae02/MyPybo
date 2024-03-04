<script>
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte"
    import { push } from "svelte-spa-router"
    export let params = {}

    let error = ''

    let token = params.token
    let password1 = ''
    let password2 = ''

    function change_password(event){
      event.preventDefault()
      fastapi("put", "/api/user/update/password/"+token, {
        password1: password1,
        password2: password2
      },
      () => {console.log('changed')},
      (err) => {error = err})
      console.log(token)
    }
</script>

<div class="container">
  <h5 class="my-3 border-bottom pb-2">비밀번호 변경</h5>
  <Error error={error} />
  <form method="post">
      <div class="mb-3">
          <label for="password1">비밀번호</label>
          <input type="text" class="form-control" id="password1" bind:value="{password1}">
      </div>
      <div class="mb-3">
          <label for="password2">비밀번호 확인</label>
          <input type="password" class="form-control" id="password2" bind:value="{password2}">
      </div>
      <button type="submit" class="btn btn-primary" on:click="{change_password}">변경하기</button>
  </form>
</div>

