
export class Book {
    id : number;
    title  : string;
    author : string;
    lang   : string;
    body   : string;   
    cover  : string
    rank   : number

    constructor(idBook?:number | any , title?:string | any, author?:string | any , lang?:string | any ,body?:string | any, cover?:string| any, rank?:number|any){ 
        this.id = idBook;
        this.title = title;
        this.author = author;
        this.lang = lang ; 
        this.body = body ; 
        this.cover = cover;
        this.rank = rank ; 
    }

}