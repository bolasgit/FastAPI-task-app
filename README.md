# FastAPI-task-app

# Alembic Notes For Data Migration

1. For alembic to work you to replace your database name from database.py in your alembic alembic.ini file (likely line 63)

2. You also need to comment out the if statement in line 14 in the env.py file in the alembic folder then align the fileConfig with the proper indentation.

3. Import your models into the env.py file in the alembic folder and input it into the target_metadata variable in line 20 by replacing your model name with "mymodel" in line

4. To run data migrations with alembic we create a new revision in terminal with the following command:
   alembic revision -m "title of revision" and enter.

5. It will create a new revision in the versions folder inside the alembic folder

6. In the newly created revision.py file created inside the versions folder, your upgrade or downgrade function will be written there.

7. The code will look like this :
   op.add_column('table_name', sa.Column('new_column_name', sa.String(255)), nullable=True)

8. In terminal you can then run the following command: alembic upgrade revision_id

9. To downgrade use the following command op.drop_column("table_name", "column_name") the run alembic downgrade -1

# PyTest Notes
