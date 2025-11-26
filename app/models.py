from app import bcrypt
from app import login_manager
from app.database import get_db
from flask_login import UserMixin
import psycopg2
import psycopg2.extras

@login_manager.user_loader
def load_user(user_id):
    return User.get_specific_id(user_id)

def create_tables(filename):
    try:
        with open(filename, 'r') as f:
            sql = f.read()
            
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        statements = sql.split(';')
        for statement in statements:
            if statement.strip():
                cur.execute(statement)
                
        conn.commit()
        cur.close()
    
        print("SQL execution was successful!")
    except Exception as e:
        print(f"An error occurred: {e}")



class User(UserMixin):
    
    def __init__(self, id=None, username=None, email=None, password=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        
    @classmethod   
    def get_all(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM users"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()

        return data 
    
    @classmethod
    def get_specific_username(cls, username):
        conn = get_db()
        cur = conn.cursor()
        query = f"SELECT * FROM users WHERE username = %s"
        cur.execute(query, (username,))
        data = cur.fetchone()
        cur.close()
        if data:
            return cls(id=data[0], username=data[1], email=data[2], password=data[3])
        return None
    
    @classmethod
    def get_specific_email(cls, email):
        conn = get_db()
        cur = conn.cursor()
        query = f"SELECT * FROM users WHERE email = %s"
        cur.execute(query, (email,))
        data = cur.fetchone()
        cur.close()
        if data:
            return cls(id=data[0], username=data[1], email=data[2], password=data[3])
        return None
    
    @classmethod
    def get_specific_id(cls, id):
        conn = get_db()
        cur = conn.cursor()
        query = f"SELECT * FROM users WHERE id= %s"
        cur.execute(query, (id,))
        data = cur.fetchone()
        cur.close()
        if data:
            return cls(id=data[0], username=data[1], email=data[2], password=data[3])
        return None
    

    
    def add(self):
        conn = get_db()
        cur = conn.cursor()
        
        password_hash = bcrypt.generate_password_hash(self.password).decode('utf-8')
        query = f"INSERT INTO users (username, email, user_password) VALUES (%s, %s, %s)"
        cur.execute(query, (self.username, self.email, password_hash))
        conn.commit()
        cur.close()
        
    def check_password(self, password_attempt):
        return bcrypt.check_password_hash(self.password, password_attempt)    
    
    @classmethod
    def delete(cls, id):
        conn = get_db()
        cur = conn.cursor()
        query = f"DELETE FROM users WHERE id = %s"
        cur.execute(query, (id,))
        conn.commit()
        cur.close()
        
    @classmethod
    def update(cls, id, username, email, password=None):
        conn = get_db()
        cur = conn.cursor()
        if password:
            query = f"UPDATE users SET username = %s, email = %s, user_password = %s WHERE id = %s"
            cur.execute(query, (username, email, password, id))
        else:
            query = f"UPDATE users SET username = %s, email = %s WHERE id = %s"
            cur.execute(query, (username, email, id))
            
        conn.commit()
        cur.close()

    def get_id(self):
        return str(self.id)
        

class Student():
    
    def __init__(self, id=None, image_url=None, image_public_id=None, first_name=None, last_name=None, gender=None, year_level=None, course_code=None):
        self.id = id
        self.image_url = image_url
        self.image_public_id = image_public_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.year_level = year_level
        self.course_code = course_code
        
    @classmethod   
    def get_all(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM students"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    
    @classmethod   
    def get_count(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT COUNT(*) FROM students"
        cur.execute(query)
        count = cur.fetchone()[0]
        cur.close()
        return count
    
    @classmethod
    def get_student_filtered(cls, search, sort, order, page, per_page):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        offset = (page - 1) * per_page
        keyword = f"%{search}%"
        
        query = f"""SELECT * FROM students 
                    WHERE CONCAT_WS(' ', id, first_name, last_name, gender, year_level, course_code) 
                    ILIKE %s ORDER BY {sort} {order}
                    LIMIT %s OFFSET %s
                """
                
        cur.execute(query, (keyword, per_page, offset))
        data = cur.fetchall()
        
        query2 = f"""SELECT COUNT(*) FROM students
                    WHERE CONCAT_WS(' ', id, pfp_url, pfp_public_id, first_name, last_name, gender, year_level, course_code)
                    ILIKE %s
                """
                
        cur.execute(query2, (keyword,))
        count = cur.fetchone()[0]
        
        cur.close()
        return data, count
    
    @classmethod
    def get_specific_student(cls, id):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM students WHERE id = %s"
        cur.execute(query, (id,))
        data = cur.fetchone()
        cur.close()
        return data
    
    def add(self):
        conn = get_db()
        cur = conn.cursor()
        
        query = """
            INSERT INTO students 
            (id, pfp_url, pfp_public_id, first_name, last_name, gender, year_level, course_code) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            self.id, 
            self.image_url, 
            self.image_public_id, 
            self.first_name, 
            self.last_name, 
            self.gender, 
            self.year_level, 
            self.course_code
        )
        cur.execute(query, data)
        conn.commit()
        cur.close()
        
    @classmethod
    def delete(cls, id):
        conn = get_db()
        cur = conn.cursor()
        query = f"DELETE FROM students WHERE id = %s"
        cur.execute(query, (id,))
        conn.commit()
        cur.close()
        
    @classmethod
    def update(cls, orig_id, id, image_url, image_public_id, name1, name2, gender, y_lvl, course):
        conn = get_db()
        cur = conn.cursor()
        query = "UPDATE students SET id = %s, pfp_url = %s, pfp_public_id = %s, first_name = %s, last_name = %s, gender = %s, year_level = %s, course_code = %s WHERE id = %s"
        cur.execute(query, (id, image_url, image_public_id, name1, name2, gender, y_lvl, course, orig_id))
        conn.commit()
        cur.close()
        
        
class Program():
    
    def __init__(self, code=None, name=None, college_code=None):
        self.code = code
        self.name = name
        self.college_code = college_code
        
    @classmethod   
    def get_all(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM program"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        
        return data
    
    @classmethod
    def get_count(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT COUNT(*) FROM program"
        cur.execute(query)
        count = cur.fetchone()[0]
        cur.close()
        return count
    
    @classmethod
    def get_program_filtered(cls, search, sort, order, page, per_page):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        offset = (page - 1) * per_page
        keyword = f"%{search}%"
        
        query = f"""SELECT * FROM program 
                    WHERE CONCAT_WS(' ', code, name, college_code) 
                    ILIKE %s ORDER BY {sort} {order}
                    LIMIT %s OFFSET %s
                """
                
        cur.execute(query, (keyword, per_page, offset))
        data = cur.fetchall()
        
        query2 = f"""SELECT COUNT(*) FROM program
                    WHERE CONCAT_WS(' ', code, name, college_code) ILIKE %s
                """
                
        cur.execute(query2, (keyword,))
        count = cur.fetchone()[0]
        
        cur.close()
        return data, count
    
    @classmethod
    def get_specific_program(cls, code):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM program WHERE code = %s"
        cur.execute(query, (code,))
        data = cur.fetchone()
        cur.close()
        return data
    
    @classmethod
    def get_specific_program_name(cls, code):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM program WHERE name = %s"
        cur.execute(query, (code,))
        data = cur.fetchone()
        cur.close()
        return data
    
    def add(self):
        conn = get_db()
        cur = conn.cursor()
        query = "INSERT INTO program (code, name, college_code) VALUES (%s, %s, %s)"
        cur.execute(query, (self.code, self.name, self.college_code))
        conn.commit()
        cur.close()
    
    @classmethod
    def delete(cls, code):
        conn = get_db()
        cur = conn.cursor()
        query = "DELETE FROM program WHERE code = %s"
        cur.execute(query, (code,))
        conn.commit()
        cur.close()
        
    @classmethod
    def update(cls, orig_code, code, name, college):
        conn = get_db()
        cur = conn.cursor()
        query = "UPDATE program SET code = %s, name = %s, college_code = %s WHERE code = %s"
        cur.execute(query, (code, name, college, orig_code))
        conn.commit()
        cur.close()
        
class College():
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name
        
    @classmethod   
    def get_all(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM college"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return data
    
    @classmethod
    def get_count(cls):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT COUNT(*) FROM college"
        cur.execute(query)
        count = cur.fetchone()[0]
        cur.close()
        return count
    
    @classmethod
    def get_college_filtered(cls, search, sort, order, page, per_page):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        offset = (page - 1) * per_page
        keyword = f"%{search}%"
        
        query = f"""SELECT * FROM college 
                    WHERE CONCAT_WS(' ', code, name) 
                    ILIKE %s ORDER BY {sort} {order}
                    LIMIT %s OFFSET %s
                """
                
        cur.execute(query, (keyword, per_page, offset))
        data = cur.fetchall()
        
        query2 = f"""SELECT COUNT(*) FROM college
                    WHERE CONCAT_WS(' ', code, name) ILIKE %s
                """
                
        cur.execute(query2, (keyword,))
        count = cur.fetchone()[0]
        
        cur.close()
        return data, count
    
    @classmethod
    def get_specific_college(cls, code):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM college WHERE code = %s"
        cur.execute(query, (code,))
        data = cur.fetchone()
        cur.close()
        return data
    
    @classmethod
    def get_specific_college_name(cls, name):
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM college WHERE name = %s"
        cur.execute(query, (name,))
        data = cur.fetchone()
        cur.close()
        return data
    
    def add(self):
        conn = get_db()
        cur = conn.cursor()
        query = "INSERT INTO college (code, name) VALUES (%s, %s)"
        cur.execute(query, (self.code, self.name))
        conn.commit()
        cur.close()
        
    @classmethod
    def delete(cls, code):
        conn = get_db()
        cur = conn.cursor()
        query = "DELETE FROM college WHERE code = %s"
        cur.execute(query, (code,))
        conn.commit()
        cur.close()
        
    @classmethod
    def update(cls, orig_code, code, name):
        conn = get_db()
        cur = conn.cursor()
        query = "UPDATE college SET code = %s, name = %s WHERE code = %s"
        cur.execute(query, (code, name, orig_code))
        conn.commit()
        cur.close()