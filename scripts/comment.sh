curl -H "Authorization: token 256203e7cc261e9343eeeeeef47129b93d096233" -X POST \
-d "{\"body\": \"Hello world\"}" \
"https://api.github.com/repos/${TRAVIS_REPO_SLUG}/issues/${TRAVIS_PULL_REQUEST}/comments"