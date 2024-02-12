'use strict';
process.stdin.resume();
process.stdin.setEncoding('utf8');

let inputString = '';
let currentLine =0;

process.stdin.on('data', function(data) {
    inputString+=data;
})
process.stdin.on('end', function() {
    inputString = inputString.trim().split('\n').map(e=>e.trim());
    main();
});

function readLine(){
    return inputString[currentLine++];
}

function printPyramid(n){
    for (let i=0;i<=n;i++){
        process.stdout.write('\n');
        for (let j=0;j<=i;j++){
            process.stdout.write(' *');
        }
    }
}

function main() {

    let t= parseInt(readLine());

    while(t--){
      let n = parseInt(readLine());
      printPyramid(n)
    }

}




