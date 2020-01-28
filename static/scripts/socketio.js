document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    //var socket = io();
    socket.on('connect', () => {
        socket.send("Iam connected");
        
    });

    socket.on('message', data =>{
        console.log(`Message  received: ${data}`)
    });
    socket.on('some-event', data => {
        console.log(data);
    });
})