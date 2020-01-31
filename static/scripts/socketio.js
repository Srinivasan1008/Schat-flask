document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    let room="Class";
    joinRoom("Class");
    //var socket = io();
   /* socket.on('connect', () => {
        socket.send("Iam connected");
        
    });*/

//display incoming msg
    socket.on('message', data =>{
        //console.log(`Message  received: ${data}`)
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if(data.username){
        span_username.innerHTML = data.username;
        span_timestamp.innerHTML = data.time_stamp;
        p.innerHTML =span_username.outerHTML +br.outerHTML + data.msg +br.outerHTML + span_timestamp.outerHTML;
        document.querySelector('#display-message-section').append(p);}
        else{
            printSysMsg(data.msg);
        }

    });
    /*socket.on('some-event', data => {
        console.log(data);
    });*/
    //send message

    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value,
        'username' : username,'room': room});
        //clear input area
        document.querySelector('#user_message').value='';
    }
    
    //room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () =>{
            let newRoom =p.innerHTML;
            if (newRoom == room){
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            }
            else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });
    //leave room
    function leaveRoom(room)
    {
         socket.emit('leave',{'username': username,'room': room});

    }
    //join room
    function joinRoom(room){
        socket.emit('join',{'username': username,'room': room});
        //clear msg area
        document.querySelector('#display-message-section').innerHTML ='';
        //autofocus on text box
        document.querySelector('#user_message').focus();
    }

    //print system message
    function printSysMsg(msg){
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
})