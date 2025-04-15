export function formateDate(str){
    let date = new Date();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    month > 10 ? month : "0" + month;
    day > 10 ? day: "0" + day;
    return month + '-' + day + " " + str;
}