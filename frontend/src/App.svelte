<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from './components/Navigation.svelte'
  import UserCreate from './routes/UserCreate.svelte'
  import UserLogin from './routes/UserLogin.svelte'
  import QuestionModify from './routes/QuestionModify.svelte'
  import AnswerModify from './routes/AnswerModify.svelte'
  import ReplyModify from './routes/ReplyModify.svelte'
  import ResetPassword from './routes/ResetPassword.svelte'
  import EnterEmail from './routes/EnterEmail.svelte';

  const routes = {
    '/': Home,
    '/detail/:question_id' : Detail,
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
    '/reply-modify/:reply_id': ReplyModify,
    '/reset-password/:token': ResetPassword,
    '/enter-email': EnterEmail,
  }
</script>

<Navigation />
<Router {routes}/>
