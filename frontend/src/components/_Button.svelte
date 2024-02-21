<script>
    export let value
    export let onclick
</script>

<button class="btn btn-sm btn-outline-secondary" on:click={onclick}>{value}</button>