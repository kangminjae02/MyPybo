class AnswerListSchema{
    constructor(question_id, answer_list){
        self.question_id = question_id
        self.answer_list = answer_list
    }
}

class AnswerSchema{
    constructor(question_id, answer){
        self.question_id = question_id
        self.answer = answer
    }
}

export {AnswerListSchema, AnswerSchema}