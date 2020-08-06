{% extends "chat/Base.html" %}
{% load static %}

{% block  content %}

        <div style="margin-top: 12px">
            <h3>{{friend.name}}</h3>
        </div>
        <div class="messages" id="board">
            {% block message %}
            {% endblock %}
        </div>
        <div class="row">
            <form method="post" class="form-group" id="chat-box">
                {% csrf_token %}
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <input type="text" placeholder="Send a message..." name="message" id="msg_field">
                        <button type="submit" name="send" class="btn btn-success" id="send_btn">Send</button>
                    </div>
                </div>
            </form>
        </div>

    <script>
        var messageBody = document.querySelector('.messages');
        messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

        sender_id = "{{ friend.id }}";
        receiver_id = "{{ curr_user.id }}";

        function scrolltoend() {
            $('#board').stop().animate({
                scrollTop: $('#board')[0].scrollHeight
            }, 800);
         }

        const text_box = '<div class="container darker">' +
            '<img src="{% static 'images/user_image.jpg' %}" alt="Avatar" class="right" style="width:100%;">' +
            '<p>{description}</p>' +
            '<span class="time-right">{time}</span>' +
            '</div>'

        //For sending
        $(function () {
            $('#chat-box').on('submit', function (event) {
                event.preventDefault();
                var message = $('#msg_field');
                send('{{ curr_user.username }}', '{{ friend.username }}', message.val());
                message.val('');
            })
        })

        function send(sender, receiver, message){

            $.post('/api/messages', '{"sender_name": "' + sender + '", "receiver_name": "' +
                    receiver + '","description": "' + message + '" }', function (data) {
                var field = text_box.replace('{description}', message);
                var today = new Date();
                var time = today.getHours() + ":" + today.getMinutes()
                field = field.replace('{time}', time)
                $('#board').append(field);
                scrolltoend();
            })
        }

    </script>

{% endblock %}
