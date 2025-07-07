from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_db

app = Flask(__name__)
app.secret_key = 'a-very-secret-key'  # used for flash messages and sessions

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jobs/<category>')
def jobs(category):
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT
          id,
          title   AS role,
          category,
          location,
          openings,
          logo_url
        FROM accorian_jobs
        WHERE category = %s
          AND company  = 'Accorian'
          AND openings > 0
    """, (category,))
    jobs = cur.fetchall()
    cur.close(); db.close()
    return render_template('jobs.html', jobs=jobs, category=category)


@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    db  = get_db()
    cur = db.cursor(dictionary=True)

    # 1) Fetch the job
    cur.execute(
        "SELECT * FROM accorian_jobs WHERE id = %s AND company = 'Accorian'",
        (job_id,)
    )
    job = cur.fetchone()

    # 2) If no such job or no openings, show no_openings page
    if not job or job['openings'] <= 0:
        cur.close(); db.close()
        return render_template('no_openings.html', job=job)

    if request.method == 'POST':
        # 3) Record the application
        name  = request.form['name']
        email = request.form['email']
        cur.execute(
            "INSERT INTO applications (job_id, name, email) VALUES (%s, %s, %s)",
            (job_id, name, email)
        )
        # 4) Decrement the openings
        cur.execute(
            "UPDATE accorian_jobs SET openings = openings - 1 WHERE id = %s",
            (job_id,)
        )
        db.commit()

        # 5) Re‐fetch the updated job so openings is fresh
        cur.execute(
            "SELECT * FROM accorian_jobs WHERE id = %s",
            (job_id,)
        )
        job = cur.fetchone()

        cur.close(); db.close()
        return render_template('success.html', job=job)

    # GET → show the apply form
    cur.close(); db.close()
    return render_template('apply_form.html', job=job)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db  = get_db()
    cur = db.cursor(dictionary=True)

    if request.method == 'POST':
        # Insert a new Accorian job with default logo
        cur.execute("""
            INSERT INTO accorian_jobs
              (title, category, location, openings, logo_url, company)
            VALUES
              (%s, %s, %s, %s, %s, 'Accorian')
        """, (
            request.form['title'],
            request.form['category'],
            request.form['location'],
            int(request.form['openings']),
            '/static/logos/accorian.png'
        ))
        db.commit()
        flash("Job posted successfully!", 'success')
        cur.close(); db.close()
        return redirect(url_for('admin'))

    # Summarize total openings per category
    cur.execute("""
        SELECT COALESCE(SUM(openings),0) AS total_openings
          FROM accorian_jobs
         WHERE category='tech' AND company='Accorian'
    """)
    tech_openings = cur.fetchone()['total_openings']

    cur.execute("""
        SELECT COALESCE(SUM(openings),0) AS total_openings
          FROM accorian_jobs
         WHERE category='non-tech' AND company='Accorian'
    """)
    nontech_openings = cur.fetchone()['total_openings']

    cur.execute("""
        SELECT COALESCE(SUM(openings),0) AS total_openings
          FROM accorian_jobs
         WHERE category='other' AND company='Accorian'
    """)
    other_openings = cur.fetchone()['total_openings']

    cur.close(); db.close()
    return render_template(
        'admin.html',
        tech_openings=tech_openings,
        nontech_openings=nontech_openings,
        other_openings=other_openings
    )


@app.route('/applications')
def view_applications():
    db  = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT
          a.name,
          a.email,
          j.title    AS job_title,
          j.category AS job_category,
          a.applied_at
        FROM applications a
        JOIN accorian_jobs j ON a.job_id = j.id
        WHERE j.company='Accorian'
        ORDER BY a.applied_at DESC
    """)
    applications = cur.fetchall()
    cur.close(); db.close()
    return render_template('applications.html', applications=applications)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
