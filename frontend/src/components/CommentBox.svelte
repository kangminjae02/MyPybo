<script>
    export let rows=1;
    export let on_submitted = () => {};
    let content = "";
</script>

<form method="post" class="my-3">
    <div class="mb-3">
        <textarea rows="{rows}" bind:value={content} class="form-control" />
    </div>
    <input
        type="submit"
        value="답변등록"
        class="btn btn-primary"
        on:click={(event) => {
            event.preventDefault();
            on_submitted(content);
            content = "";
        }}
    />
</form>
