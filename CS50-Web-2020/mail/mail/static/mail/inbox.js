document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // document.querySelector('#compose-form').onsubmit = send_email();

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#content-view').style.display = 'none';

  document.querySelector('#compose-recipients').value = "";
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email(e) {
  // prevent default redirection of form to inbox
  e.preventDefault();
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    //after error, how to not redirect to inbox page?
    console.log(result);
    if (result.error) {
      console.log(result.error);
      document.querySelector('#compose-error').innerHTML = result.error.fontcolor("red");
      // alert(result.error);
    } else {
      document.querySelector('#compose-error').innerHTML = "";
      // Doesnt load to sent leh
      load_mailbox("sent");
      alert("Message sent Successfully");
    }
  });

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox == "inbox") {
    fetch(`/emails/inbox`)
    .then(response => response.json())
    .then(data => {
      data.forEach((element) => {
        var item = document.createElement("div");
        item.innerHTML = 
        `<div class="card">
        <div class="card-body">
        <h5 class="card-title">${element.subject} </h5>
        <h6 class="card-subtitle mb-2 text-muted">${element.sender}, ${element.timestamp} </h6>
        <p>${element.body.slice(0, 50)}</p>
        </div>
        </div>`;
        if (`${element.read}` == "true") {
          item.className = "card bg-light mb-3";
        } else {
          item.className = "card bg-secondary mb-3";
        }
        item.addEventListener('click', () => view_mail(element.id));
        document.querySelector("#emails-view").appendChild(item);
        console.log(data);
      });
    })
    .catch(error => {
      console.log('Error: ', error);
    });
  } else if (mailbox == "sent") {
    fetch(`/emails/sent`)
    .then(response => response.json())
    .then(data => {
      data.forEach((element) => {
        var item = document.createElement("div");
        item.innerHTML = 
        `<div class="card">
        <div class="card-body">
        <h5 class="card-title">${element.subject} </h5>
        <h6 class="card-subtitle mb-2 text-muted">Sent to: ${element.recipients}, ${element.timestamp} </h6>
        <p>${element.body}</p>
        </div>
        </div>`;
        item.addEventListener('click', () => view_mail(element.id));
        document.querySelector("#emails-view").appendChild(item);
        console.log(data);
      });
    })
    .catch(error => {
      console.log('Error: ', error);
    });    
  } else {
    fetch(`/emails/archive`)
    .then(response => response.json())
    .then(data => {
      data.forEach((element) => {
        var item = document.createElement("div");
        item.innerHTML = 
        `<div class="card">
        <div class="card-body">
        <h5 class="card-title">${element.subject} </h5>
        <h6 class="card-subtitle mb-2 text-muted">Sent to: ${element.recipients}, ${element.timestamp} </h6>
        <p>${element.body}</p>
        </div>
        </div>`;
        item.addEventListener('click', () => view_mail(element.id));
        document.querySelector("#emails-view").appendChild(item);
        console.log(data);
      });
    })
    .catch(error => {
      console.log('Error: ', error);
    });    
  }
}

function view_mail(element){
  console.log(`clicked ${element}`);
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'block';
  document.querySelector("#content-view").innerHTML="";
  fetch(`/emails/${element}`)
  .then(response => response.json())
  .then(email => {
    const item = document.createElement("div");
    console.log(email);
    item.innerHTML = 
    `<div class="card-body">
    <h5 class="card-title">${email.subject} </h5>
    <h6 class="card-subtitle mb-2 text-muted">From: ${email.sender}<br>To: ${email.recipients}<br>${email.timestamp} </h6>
    <p>${email.body}</p>
    </div>`;
    document.querySelector("#content-view").append(item);
    const reply = document.createElement("BUTTON");
    reply.className = "btn btn-Light";
    reply.style = "color:blue";
    reply.innerHTML = "Reply";
    document.querySelector("#content-view").append(reply);
    if (email.archived) {
      const unarchive = document.createElement("BUTTON");
      unarchive.className = "btn btn-Light";
      unarchive.style = "color:blue";
      unarchive.innerHTML = "Unarchive";
      document.querySelector("#content-view").append(unarchive);
      unarchive.addEventListener("click", () => set_archive(email.id, email.archived));
    } else {
      const archive = document.createElement("BUTTON");
      archive.className = "btn btn-Light";
      archive.style = "color:blue";
      archive.innerHTML = "Archive";
      document.querySelector("#content-view").append(archive);
      archive.addEventListener("click", () => set_archive(email.id, email.archived));
    }
    set_read(email.id);
    reply.addEventListener("click", () => reply_email(email.sender, email.subject, email.body, email.timestamp));
  })
  .catch(error => {
    console.log('Error: ', error);
  });
}

function set_archive(email_id, archived){
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !archived,
    }),
  })
  .catch(error => {
    console.log('Error: ', error);
  });
  console.log(archived);
  view_mail(email_id);
}

function set_read(email_id) {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
}

function reply_email(sender, subject, body, timestamp) {
  compose_email();
  if (!/^Re:/.test(subject)) subject = `Re: ${subject}`;
  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subject;

  pre_body = `On ${timestamp} ${sender} wrote:\n${body}\n`;

  document.querySelector("#compose-body").value = pre_body;
  // load_mailbox("sent");
}