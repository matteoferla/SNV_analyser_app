$("[data-toggle='user']").click(function () {
    var li = $(this).parent();
    $.ajax({url: "/login",
            data: {username: $(this).data('target'),
                   password: null,
                   action: 'promote'},
            method: 'POST'
        })
        .done(function (msg) {
            console.log(msg);
            li.children('span').children('i').removeClass('fa-user').addClass('fa-user-crown');
            li.children('button').detach();
        });
    });
