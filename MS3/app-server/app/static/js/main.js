/*
 * Updates a <li> task when clicking on the "redo" button
 */

function updateTask (taskId, action) {
    $.ajax({
      url: '/taskop',
      method: 'POST',
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify({ op: "UPDATE", 
                             action: action, 
                             task_id: taskId})
    })
    .done(function (result) {
      console.log(result);
    })
}

/*
 * Deletes a <li> task when clicking on the "X" button
 */
function deleteTask (liTag) {
    var taskId = liTag.attr('id');
    $.ajax({
      url: '/taskop',
      method: 'POST',
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify({ op: "DELETE", 
                             action: "Some Action",
                             task_id: parseInt(taskId)})
    })
    .done(function (result) {
      liTag.remove();
    });
}

/*
 * Create a new <li> task when clicking on the "Add" button
 */
function createNewTask() {
  var inputValue = $("#taskInput").val();
  if (inputValue === '') {
      alert("You must write something!");
  } else {
    console.log('Creating new task', inputValue);
    $.ajax({
      url: '/taskop',
      method: 'POST',
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify({ op: "ADD", action: inputValue })
    })
    .done(function (result) {
      // XXX: Explain chaining
      var newTask = result.task;
      $('<li/>', {
        id: newTask.task_id,
      }).appendTo('#myUL')

      // Add the span
      $('<span/>', {
        text: "✘ ",
        "class": "close"
      })
      .appendTo('#' + newTask.task_id)
      .click(onCloseHandler)

      $('<span/>', {
        text: "↺ ",
        "class": "updater",
      })
      .appendTo('#' + newTask.task_id)
      .click(onUpdateHandler)

      $('<span/>', {
        text: newTask.action,
        "class": "action"
      })
      .appendTo('#' + newTask.task_id)

      $('<input/>', {
        value: newTask.action,
        "class": "updateAction"
      })
      .appendTo('#' + newTask.task_id)
      .hide()

      // Remove the input that you just entered
      $("#taskInput").val('');
    });

  }
}

/* Common Handler code */
function onCloseHandler () {
  var liTag = $(this).parent('li');
  deleteTask(liTag);
}

function onUpdateHandler (event) {
  var liTag = $(this).parent('li');
  var spanTag = $(this).siblings('.action');
  var inputTag = $(this).siblings('.updateAction');
  if (inputTag.is(':visible')) {
    var taskId = parseInt(liTag.attr('id'));
    var action = inputTag.val()
    updateTask(taskId, action);
    inputTag.hide();
    spanTag.text(action);
    spanTag.show();
    liTag.toggleClass('checked', false);
  } else {
    // Why do we need this?
    inputTag.css('display', 'inline');
    spanTag.hide();
    liTag.toggleClass('checked', false);
  }
  // What is the purpose of this?
  event.stopPropagation();
  event.cancelBubble = true;  // Deprecated but for legacy browsers
}

/* This is the entry point for our dynamic behavior */
$(document).ready(function () {
  // Every close button when clicked will delete itself from the list
  // and submit a call to the API to self-delete.
  $('.close').each(function (i, el) {
    // Why do we need this bind?
    el.onclick = onCloseHandler.bind(this)
  })

  $('.updater').each(function (i, el) {
    el.onclick = onUpdateHandler.bind(this);
  })

  $('li').each(function (i, el) {
    el.onclick = function() {
      var inputTag = $(this).children('input');
      if (!inputTag.is(':visible')) {
        $(this).toggleClass('checked');
      }
    };
  });
});
