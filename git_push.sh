#Provide first agrument as file to be added to the repo
filename=$1
git add $filename

#Adding comments for the git push to repo
msg=$2
git commit -m "$msg"

#Pushing the file to git repo
git push
