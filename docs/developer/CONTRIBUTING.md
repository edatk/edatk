# Contributing

1. Fork the repo to your profile (top right in Github).
1. cd into your local directory and setup a local repo with git clone.
    ```
    git clone https://github.com/YOUR_USERNAME/edatk.git
    ```
1. Ensure remote is setup to your repo.
    ```
    git remote -v
    ```
1. Running the above step, you should see something like the following:
    ```
    origin  https://github.com/YOUR_USERNAME/edatk.git (fetch)
    origin  https://github.com/YOUR_USERNAME/edatk.git (push)
    ```
1. Setup your upstream connection to the main organization repo. This will allow you to pull down changes and keep up-to-date while developing.
    ```
    git remote add upstream https://github.com/edatk/edatk.git
    ```
1. Rerun git remote -v and you should now see the following
    ```
    origin  https://github.com/YOUR_USERNAME/edatk.git (fetch)
    origin  https://github.com/YOUR_USERNAME/edatk.git (push)
    upstream        https://github.com/edatk/edatk.git (fetch)
    upstream        https://github.com/edatk/edatk.git (push)
    ```
1. Create a new branch to hold your changes. Never do your development work on the main branch.
    ```
    git checkout -b "my_changes"
    ```
1. Do your development work on this branch and commit your changes.
    ```
    git status
    git add -A
    git commit -m "my changes"
    ```
1. Before pushing changes to your repo, make sure to sync any changes from upstream. You may be out of date and this will ensure no conflicts.
    ```
    git checkout main
    git fetch upstream
    git merge upstream/main
    git checkout my_changes
    git merge main
    ```
1. Resolve any conflicts from above step, accepting incoming change from upstream where possible. If any conflicts resulted, you may need to re-merge.
    ```
    git add -A
    git commit -m "my changes-fixing merge conflicts"
    ```
1. View files changed to ensure as expected.
    ```
    git diff --name-only main my_changes
    ```
1. Push your changes to your repo.
    ```
    git push origin main
    ```
1. Go to your github repo in your browser and submit a pull request describing your changes. Leave your branch open until merged. After that point, you are free to fetch to resync if you're working on additional changes, delete your personal forked repo, etc.
