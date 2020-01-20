// This is the controller for the login-page of an android app I built.
// It implements Firebase to authenticate and then get user info for display
// on the next page. I've removed all of the imports to save some room at the top. 


public class LoginActivity extends AppCompatActivity implements ListenerActivity {
    private FirebaseAuth fbAuth;
    private FirebaseUser currentUser;
    private FirebaseFirestore db;
    private View loadingScreen;
    private ProgressBar progressBar;
    private EditText emailET;
    private EditText passwordET;

    // =================== LIFECYCLE ===================
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        fbAuth = FirebaseAuth.getInstance();
        startListeners();
    }

    @Override
    protected void onResume() {
        super.onResume();
        currentUser = fbAuth.getCurrentUser();
        if (currentUser != null) {
            fbAuth.signOut();
        }
    }


    // =================== METHODS ===================
    private void attemptLogin() {
        String email = emailET.getText().toString();
        String password = passwordET.getText().toString();

        // Validate input
        if (!InputValidations.validateEmail(email)) {
            Toast.makeText(this, getString(R.string.badFormatEmail), Toast.LENGTH_SHORT).show();
            return;
        }

        if (!InputValidations.validatePassword(password)) {
            Toast.makeText(this, getString(R.string.badFormatPassword), Toast.LENGTH_SHORT).show();
            return;
        }


        // Attempt login
        Utils.hideKeyboard(getApplicationContext(), loadingScreen);
        Utils.startLoadingScreen(loadingScreen, progressBar);
        fbAuth.signInWithEmailAndPassword(email,password).addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                db = FirebaseFirestore.getInstance();
                String id = fbAuth.getUid();
                if (id != null) {
                    DocumentReference docRef = db.collection(FirebaseString.users).document(id);
                    docRef.get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                        @Override
                        public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                            DocumentSnapshot docSnap = task.getResult();
                            if (docSnap != null && docSnap.exists()) {
                                sendToNextActivity(docSnap);
                            }else {
                                Utils.toast(getApplicationContext(), getString(R.string.loggedInButCantFindInDatabase));
                            }
                            Utils.endLoadingScreen(loadingScreen, progressBar);
                        }
                    }).addOnFailureListener(new OnFailureListener() {
                        @Override
                        public void onFailure(@NonNull Exception e) {
                            Toast.makeText(getApplicationContext(), getString(R.string.loggedInButCantFindInDatabase), Toast.LENGTH_SHORT).show();
                        }
                    });
                }
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                handleFailure(e);
            }
        });
    }

    private void sendToNextActivity(DocumentSnapshot docSnap) {
        Map m = docSnap.getData();
        String userType = m.get(FirebaseString.userType).toString();
        SharedPreferences preferences = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        if (userType.equals(getString(R.string.userTypeTeacher))) {
            ArrayList data = (ArrayList) m.get(FirebaseString.students);
            List<Student> students = new ArrayList<>();

            for (Object o:data) {
                HashMap map = (HashMap) o;
                String name = (String) map.get(FirebaseString.studentName);
                String id = (String) map.get(FirebaseString.studentId);
                String email = (String) map.get(FirebaseString.studentEmail);
                Student student = new Student(name, id);
                students.add(student);
            }
            Teacher  t = docSnap.toObject(Teacher.class);
            t.setStudents(students);
            Utils.saveCurrentTeacherInSharedPreferences(preferences,t);
            Intent intent = new Intent(this, StudentListActivity.class);
            startActivity(intent);

        } else if (userType.equals(getString(R.string.userTypeStudent))) {
            Student s = docSnap.toObject(Student.class);
            Intent intent = new Intent(this, SubjectListStudentActivity.class);
            Utils.saveCurrentStudentInSharedPreferences(preferences, s);
            startActivity(intent);
        }
    }

    private void handleFailure(Exception e) {
        if (e instanceof FirebaseAuthInvalidCredentialsException) {
            Toast.makeText(getApplicationContext(), getString(R.string.wrongPassword), Toast.LENGTH_SHORT).show();
        } else if (e instanceof FirebaseAuthInvalidUserException) {
            String errorCode = ((FirebaseAuthInvalidUserException) e).getErrorCode();
            if (errorCode.equals(FirebaseString.errorUserNotFound)) {
                Toast.makeText(getApplicationContext(), getString(R.string.wrongEmail), Toast.LENGTH_SHORT).show();
            } else if (errorCode.equals(FirebaseString.errorUserDisabled)) {
                Toast.makeText(getApplicationContext(), getString(R.string.accountDisabled), Toast.LENGTH_SHORT).show();
            }
        } else {
            Toast.makeText(getApplicationContext(), getString(R.string.somethingWrong), Toast.LENGTH_SHORT).show();
        }
        Utils.endLoadingScreen(loadingScreen, progressBar);
    }

    private void sendToForgotPasswordActivity() {
        Intent intent = new Intent(this, ForgotPasswordActivity.class);
        startActivity(intent);
    }

    private void sendToNewUserActivity() {
        Intent intent = new Intent(this, NewUserActivity.class);
        startActivity(intent);
    }

    @Override
    public void startListeners() {
        loadingScreen = findViewById(R.id.loading_screen);
        progressBar = findViewById(R.id.loading_screen_progressbar);

        Button loginBtn = findViewById(R.id.LoginActivity_Button_Login);
        loginBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                attemptLogin();
            }
        });

        Button newUserBtn = findViewById(R.id.LoginActivity_Button_NewUser);
        newUserBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendToNewUserActivity();
            }
        });

        Button forgotPasswordBtn = findViewById(R.id.LoginActivity_Button_ForgotPassword);
        forgotPasswordBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendToForgotPasswordActivity();
            }
        });

        emailET = findViewById(R.id.LoginActivity_EditText_Email);
        emailET.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View view, int i, KeyEvent keyEvent) {
                if (i == KeyEvent.KEYCODE_ENTER && keyEvent.getAction() == KeyEvent.ACTION_UP) {
                    passwordET.requestFocus();
                }
                return false;
            }
        });

        passwordET = findViewById(R.id.LoginActivity_EditText_Password);
        passwordET.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View view, int i, KeyEvent keyEvent) {
                if (i == KeyEvent.KEYCODE_ENTER && keyEvent.getAction() == KeyEvent.ACTION_UP) {
                    attemptLogin();
                }
                return false;
            }
        });

    }
}
