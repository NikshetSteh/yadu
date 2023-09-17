# Skill state
This is an object that stores information about the user. The data inside it is divided into three, depending 
on the storage context of the session: user application instance, authorized user

## Fields:
- `session_vars` - session context
- `user_vars` - authorized user context
- `application_vars` - application instance context