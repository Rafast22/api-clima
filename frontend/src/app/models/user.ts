export class User {
    username?: string;
    password?: string;
    full_name?: string;
    email?: string;
    is_staff:boolean =  false;
    is_active:boolean =  true;
    role:string =  "user";
    constructor(user:any){
        this.generateUsername(user.email);
        this.password = user.password
        this.full_name = user.full_name
        this.email = user.email
    }
    private generateUsername(email:string):void{
        const e = email.split("@");
        if(e.length > 0 )
            this.username = email;
    }
}
