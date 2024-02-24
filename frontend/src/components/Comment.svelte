<script>
    import CommentBox from "./CommentBox.svelte";

    export let username='소년';
    export let content='';
    export let created_date='2000-00-00';
    export let modified_date;
    export let login_id;
    export let recommend_count=0
    export let on_recommended;
    export let on_modified;
    export let on_deleted;
    export let on_replied;

    let is_visible_commentbox = false
</script>

<div class="card">
    <div class="card-header">
        {username}
    </div>
    <div class="card-body">
        <p class="card-text">
            {content}
        </p>
        <button on:click={on_recommended()}>추천</button> {recommend_count}
        {#if login_id === username}
        <button on:click={on_modified()}>수정</button>
        <button on:click={on_deleted()}>삭제</button>
        {/if}
        {#if on_replied}
        <button on:click={() => {is_visible_commentbox = is_visible_commentbox ? false:true}}>답변</button>
        {/if}
        {#if is_visible_commentbox}
        <CommentBox 
            rows={1}
            on_submitted={
                (content) => {
                    on_replied(content)
                    is_visible_commentbox=false
                }
            }
        />
        {/if}
    </div>
    <div class="card-footer text-body-secondary text-end">
        {created_date}
        {modified_date}
    </div>
</div>