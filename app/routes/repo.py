from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.repo import repository
from app.models.user import User
from datetime import datetime , timedelta
from app.models.commit import Commit

import smtplib
from app.utils.github import fetch_last_hour_commits
from email.mime.text import MIMEText
import requests

from app.utils.send_email import send_email
from app.utils.slack import send_slack_message
import os

router = APIRouter(prefix="/repo")

@router.post("/add")
def add_repo(user_id : int , name : str , owner:str , db : Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "the user is not authorized"
        )
    
    repo = repository(name = name , owner = owner  , user_id = user_id , last_synced_at = datetime.utcnow())

    db.add(repo)
    db.commit()
    db.refresh(repo)

    return {"messge" : "repo added successfully " , "repo_id" : repo.id}


@router.post("/sync/{repo_id}")
def sync_commits(repo_id : int , db : Session = Depends(get_db)):



    repo = db.query(repository).filter(repository.id == repo_id).first()

    if not repo:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "this id is not authorized"
        )

    if repo.last_synced_at:
        since = repo.last_synced_at
    else:

        since = datetime.utcnow() - timedelta(hours=1)
    commits = fetch_last_hour_commits(repo.owner , repo.name , since)

    new_commits = 0
    email_body = ""

    for c in commits:
        sha = c["sha"]



        exists = db.query(Commit).filter(Commit.sha == sha).first() 

        if exists:
            continue

        commit = Commit(
            sha = sha,
            author = c["commit"]["author"]["name"],
            email = c["commit"]["author"]["email"],


            message = c["commit"]["message"], 
            commit_time = datetime.fromisoformat (c["commit"]["author"]["date"].replace("Z" , "")),

            repo_id = repo.id

        )

        db.add(commit)
        new_commits += 1

        # message=(
        #     f"repository : {repo.name}\n"
        #     f"author name : {commit.author}\n"
        #     f"author email : {commit.email}\n"
        #     f"time : {commit.commit_time}"

        #     f"message : {commit.message}"

        # )

        email_body += (
            f"Repository: {repo.name}\n"
            f"Author Name: {commit.author}\n"
            f"Author Email: {commit.email}\n"
            f"Time: {commit.commit_time}\n"
            f"Message: {commit.message}\n"
            f"{'-'*50}\n"
        )

        db.commit()
        repo.last_synced_at = datetime.utcnow()
        db.commit()

        # try:
        #     print(f"Sending email for commit {commit.sha}...")
        #     send_email(
        #     to_email="devanshlamaniya1@gmail.com",
        #     subject=f"New commit in {repo.name}",
        #     body=message
        #     )
        #     print("Mail sent successfully.")
        # except Exception as e:
        #     print(f"Email failed for commit {commit.sha}:", e)

        # if new_commits == 0:
        #     try:
        #         print("No new commits. Sending 'no commits' email...")
        #         send_email(
        #             to_email="abhay.shukla@gammaedge.io",
        #             subject=f"No new commits in {repo.name}",
        #             body=f"There were no new commits in the repository {repo.name} since last sync."
        #         )
        #         print("No-commit email sent successfully.")
        #     except Exception as e:
        #         print("Failed to send no-commit email:", e)

    # if commits:

    if new_commits == 0:
        email_body = f"There were no new commits in the repository {repo.name} since last sync."
        subject = f"No new commits in {repo.name}"
    else:
        subject = f"{new_commits} new commit(s) in {repo.name}"

    # Send email once
    try:
        print("Sending summary email...")
        send_email(
            to_email="devanshlamaniya@gmail.com ",
            subject=subject,
            body=email_body
        )
        print("Summary email sent successfully.")
    except Exception as e:
        print("Failed to send summary email:", e)

    return {
        "message": "Sync complete",
        "new_commits": new_commits
    }
    # repo.last_synced_at = datetime.utcnow()

    # db.commit()

    # return {
    #         "message" : "sync complete",
    #         "new_commits" : new_commits
    # }

