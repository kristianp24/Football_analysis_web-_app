
class Utils
{
    static checkEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    static checkPassword(password) {
        return password.length >= 8;
    }

    static checkName(name) {
        return name.length > 0;
    }

    static checkSurname(surname) {
        return surname.length > 0;
    }

    static checkConfirmPassword(password, confirmPassword) {
        return password === confirmPassword;
    }

    static checkEmptyField(field) {
        return field.length > 0;
    }

    static checkforNumbers(field) {
        const re = /^[0-9]+$/;
        return re.test(field);
    }

    static checkIfProfessor(email){
        if (email.includes("profesor") || email.includes("prof")) {
            return true;
        }
        else {
            return false;
        }
    }

    static checkIfIncludesASE(email){
        if (email.includes("@stud.ase.ro") || email.includes("@prof.ase.ro")) {
            return true;
        }
        else {
            return false;
    }
   }

   static checkIfEmailHasAccount(emailDB, emailInput){
      return emailDB === emailInput;
   }

   static checkIfUserExists(users, email){
      for(const user of users){
         if (user['email'] === email)
            return user
      }
      return null;
   }
}
export default Utils;
