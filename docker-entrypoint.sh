#!/bin/bash -x
if [ "$ENVIRONMENT" != "test" ];then
    python manage.py migrate --noinput || exit 1
fi

# Adds reference/link of all static files to a single file.
python3 manage.py collectstatic --noinput --clear --link

echo "Starting server..."
exec "$@"