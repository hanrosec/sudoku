const start = Date.now();

const metas = document.querySelectorAll('meta[name^="g:"]');
const solution_hash = metas[0].content
const parsed_puzzle = metas[1].content

function send_to_leaderboard() {
    const end = Date.now();
    const time = end - start;

    let result_object = {
        time: time
    }

    console.log(result_object);
    let inputs = document.querySelectorAll('input#numer');
    let values = new Array();
    for (const i of inputs.values()) {
        values.push(i.value);
    }

    let solution = parsed_puzzle;
    for(let i of values) {
        solution = solution.replace("0", i);
    }

    result_object.user_hash = sha512(solution);
    result_object.system_hash = solution_hash;
    result_object.control_hash = sha512(result_object.time.toString() + result_object.user_hash + result_object.system_hash);
    $.redirect("/game/add_to_leaderboard", result_object, "POST");
}