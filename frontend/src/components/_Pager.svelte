<script>
  export let page = 0
  export let total_page = 0
  export let begin
  export let prev
  export let move
  export let next
  export let end
</script>

<ul class="pagination justify-content-center">
    <!-- 처음 페이지 -->
    <li class="page-item {page <= 0 && 'disabled'}">
      <button class="page-link" on:click="{(page) => begin}">처음</button>
    </li>
    <!-- 이전 페이지 -->
    <li class="page-item {page <= 0 && 'disabled'}">
      <button class="page-link" on:click="{(page) => prev}">이전</button>
    </li>
    <!-- 페이지 번호 -->
    {#each Array(total_page) as _, loop_page}
        {#if loop_page >= page-5 && loop_page <= page+5}
        <li class="page-item {loop_page === page && 'active'}">
        <button on:click="{(loop_page) => {move}}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
    {/each}
    <!-- 다음 페이지 -->
    <li class="page-item {page >= total_page-1 && 'disabled'}">
      <button class="page-link" on:click="{(page) => {next}}">다음</button>
    </li>
    <!-- 마지막 페이지-->
    <li class="page-item {page >= total_page-1 && 'disabled'}">
      <button class="page-link" on:click="{(page) => {end}}">마지막</button>
    </li>
</ul>