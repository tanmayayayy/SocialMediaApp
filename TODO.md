# Fix Get Posts with Votes Join
Status: Complete

## Steps:
- [x] Create this TODO.md
- [x] Edit app/routers/post.py to fix get_posts query
- [x] Test endpoint: uvicorn app.main:app --reload, GET /posts?limit=3&skip=0&search=
- [x] Mark complete, attempt_completion

Details: Minimal fix - joined vote count query with filter/search/limit/offset/order, return results.

