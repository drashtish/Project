from app import c_app
from worker import contextedTask
from mail import mailer
from flask_mail import Message
from datetime import date, datetime
from model import *
from jinja2 import Template
import flask_excel as excel
import csv



@c_app.task(base=contextedTask)
def mail_reminder():
    date_format = "%Y-%m-%d"
    today = date.today()

    issued_books = db.session.query(issuebook).all()

    overdue_books = []
    for issue in issued_books:
        if issue.dor != None and issue.cstatus == 'Approved':
            return_date = datetime.strptime(issue.dor, date_format).date()
            if (return_date - today).days == 1:
                overdue_books.append(issue)

    mail_id = []

    for usr in overdue_books:
        u = user.query.filter_by(ID=usr.uid).first()
        mail_id.append(u.Email)


    subject = 'Reminder Mail'
    body = 'Hi, This is an mail to remind you that you have not returned your book. Please return it as soon as possible.'
    msg = Message(subject=subject, recipients=mail_id, body=body)
    mailer.send(msg)
    return 'ok'





@c_app.task(base=contextedTask)
def mail_report():
    # a = user.query.all()
    # s= section.query.all()
    # b = book.query.all()
    # ib = issuebook.query.all()

    # d= {}
    # for i in ib:
    #     if i.cstatus == 'Approved':
    #         d[i.bid] = d.get(i.bid, 0) + 1

    # d= {}
    # for i in ib:
    #     d[i.bid] = (0,0)
    #     a1 = issuebook.query.filter_by(bid=i.bid, cstatus='Approved').all()
    #     a2 = issuebook.query.filter_by(bid=i.bid, cstatus='Pending').all()
    #     d[i.bid] = (len(a1), len(a2))

    # print(d)
    total_users = user.query.count()  # Count total number of users
    total_books = book.query.count()  # Count total number of books
    total_sections = section.query.count() 

    sections = section.query.all()  # Get all sections
    for sec in sections:
        sec.books = book.query.filter_by(Section=sec.ID).all()  # Get books for each section
        for b in sec.books:
            b.issues = issuebook.query.filter_by(bid=b.ID).all()  # Get issues for each book
            b.reviews = review.query.filter_by(bid=b.ID).all()



    subject = 'Monthly Report'
    email_body = 'This is an monthly report.Please check the attachment'

    body = '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="mt-5">Library Dashboard</h1>

         <div class="statistics mt-4">
            <h3>Statistics</h3>
            <ul class="list-group">
                <li class="list-group-item">Total Users: {{ total_users }}</li>
                <li class="list-group-item">Total Books: {{ total_books }}</li>
                <li class="list-group-item">Total Sections: {{ total_sections }}</li>
            </ul>
        </div>

        <hr>
        <h3>More Details</h3>

        {% for section in sections %}
        <div class="section mt-4">
            <h2>Section Name : {{ section.Title }}</h2>
            <p>Description : {{ section.Description }}</p>

            {% if section.books %}
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Book Title</th>
                        <th>Author</th>
                        <th>Pending Requests</th>
                        <th>Approved Requests</th>
                        <th>Reviews</th>
                    </tr>
                </thead>
                <tbody>
                    {% for book in section.books %}
                    <tr>
                        <td>{{ book.Title }}</td>
                        <td>{{ book.Author }}</td>
                        <td>
                            {{ book.issues | selectattr("cstatus", "equalto", "Pending") | list | length }}
                        </td>
                        <td>
                            {{ book.issues | selectattr("cstatus", "equalto", "Approved") | list | length }}
                        </td>
                        <td>
                            <ul>
                                {% for review in book.reviews %}
                                <li>{{ review.Review }} (by User ID: {{ review.uid }})</li>
                                {% endfor %}
                            </ul>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p>No books available in this section.</p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>

    '''

    template = Template(body)
    body = template.render(sections=sections, total_users=total_users, total_books=total_books, total_sections=total_sections)


    msg = Message(subject = subject, recipients=['drashti@gmail.com'], body = email_body)
    msg.html = body
    # msg.attach('file_name', "type")
    mailer.send(msg)

    return 'done'
    


# {% for i in ib %}{% if i.bid|int == j.ID|int %}{% if ib.cstatus == 'Pending' %}{%set pcount.val = pcount.val+ 1%}{% endif %}{% endif %}{% endfor %}
# {% for i in ib %}{% if i.bid|int == j.ID|int %}{% if ib.cstatus == 'Approved' %}{%set rcount.val = rcount.val+ 1%}{% endif %}{% endif %}{% endfor %}





@c_app.task(ignore_result=False)
def create_csv():
    # Perform a join between `issuebook`, `user`, and `book` tables
    res = (db.session.query(
            user.Name,
            book.Title,
            issuebook.doi,
            issuebook.dor,
            issuebook.cstatus
        )
        .join(issuebook, user.ID == issuebook.uid)
        .join(book, issuebook.bid == book.ID)
    ).all()

    # Define the CSV file path
    file_path = './export/file.csv'

    # Write the CSV file manually
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['User Name', 'Book Title', 'Date of Issue', 'Date of Return', 'Approval Status'])

        # Write the data rows
        for r in res:
            csvwriter.writerow([r.Name, r.Title, r.doi, r.dor, r.cstatus])

      # Read the CSV file to get the data for attachment
    with open(file_path, 'rb') as f:
        csv_data = f.read()

    subject = 'CSV File'
    body = 'Hi, Please check the attachment'
    msg = Message(subject=subject, recipients=['drashti@gmail.com'], body=body)
    msg.attach('file.csv', 'text/csv', csv_data)

    mailer.send(msg)
    return file_path

    # attach the file to the email



