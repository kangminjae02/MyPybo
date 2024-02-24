<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, is_login, keyword } from '../lib/store' 
    import moment from 'moment/min/moment-with-locales'
    import Pager from "../components/Pager.svelte";
    moment.locale('ko')

    let question_list = []
    let size = 10
    let total = 0
    let kw = ''
    $: total_page = Math.ceil(total/size)
    $: $page, $keyword, get_question_list()
    function get_question_list(){
      let params = {
        page: $page,
        size: size,
        keyword: $keyword,
      }
      fastapi('get', '/api/question/list', params, (json) => {
        question_list = json.question_list
        total = json.total
        kw = $keyword
      })
    }
</script>

<div class="container my-3">
  <div class="row my-3">
    <div class="col-6">
      <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
    </div>
    <div class="col-6">
      <div class="input-group">
        <div class="input-group">
          <input type="text" class="form-control" bind:value="{kw}">
          <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>찾기</button>
        </div>
      </div>
    </div>
  </div>
  <table class="table">
    <thead>
      <tr class="text-center table-dark">
        <th>번호</th>
        <th style="width:50%">제목</th>
        <th>글쓴이</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
      <tr class="text-center">
        <td>{ total - ($page*size) - i}</td>
        <td class="text-start">
          <a use:link href="/detail/{question.id}">{question.subject}</a>
          {#if question.answers.length > 0}
          <span class="text-danger small mx-2">{question.answers.length}</span>
          {/if}
        </td>
        <td>{question.user ? question.user.username : ""}</td>
        <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
      </tr>
      {/each}
    </tbody>
  </table>
  <Pager
    page={$page}
    total_page={total_page}
    on_changed={
      (_page) => {
        $page = _page
      }
    }
  />
</div>
  