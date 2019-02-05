// Controller for the loginscreen of an app I built called Bicco. 
// Contains firebase integration and basic functionality.

package se.bicco.bicco;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

import se.bicco.bicco.NewQuote.NewQuoteACT;
import se.bicco.bicco.Utilities.Util;

public class LoginACT extends AppCompatActivity {

    private FirebaseAuth mAuth;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_act);

        ImageView logo = (ImageView) findViewById(R.id.IVloginLogo);
        Glide.with(this)
                .load(R.drawable.bicco_logo_see_through)
                .into(logo);

        mAuth = FirebaseAuth.getInstance();


    }


    public void loginBTNPressed (View view) {
        EditText ETEmail = (EditText) findViewById(R.id.loginUsername);
        EditText ETPassword = (EditText) findViewById(R.id.loginPassword);

        if (ETEmail.getText().toString().equals("") || ETPassword.getText().toString().equals("")) {
            Toast.makeText(this, R.string.incorrect_email_or_password, Toast.LENGTH_SHORT).show();
        } else {

            mAuth.signInWithEmailAndPassword(ETEmail.getText().toString(), ETPassword.getText().toString())
                    .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            Log.d("Test", "signInWithEmail:onComplete:" + task.isSuccessful());

                            if (!task.isSuccessful()) {

                                if (Util.checkConnection(getApplicationContext())) {
                                    Log.w("Test", "signInWithEmail:failed", task.getException());
                                    Toast.makeText(getApplicationContext(), R.string.incorrect_email_or_password,
                                            Toast.LENGTH_SHORT).show();
                                } else {
                                    Toast.makeText(getApplicationContext(), R.string.no_network_connection, Toast.LENGTH_SHORT).show();
                                    Log.w("Test", "signInWithEmail:failed", task.getException());
                                }


                            } else {

                                Util.firebaseGetAndSetHourlyFee(getApplicationContext());

                                Intent newQuote = new Intent(getApplicationContext(), NewQuoteACT.class);
                                newQuote.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
                                startActivity(newQuote);

                                finish();
                            }
                        }
                    });

        }


    }

    public void registerBTNPressed (View view) {
        EditText ETEmail = (EditText) findViewById(R.id.loginUsername);
        EditText ETPassword = (EditText) findViewById(R.id.loginPassword);

        Intent register = new Intent(this, RegisterACT.class);
        register.putExtra(getString(R.string.username), ETEmail.getText().toString());
        register.putExtra(getString(R.string.password), ETPassword.getText().toString());
        register.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
        startActivity(register);
    }

    public void goToForgotPassword (View view) {
        EditText ETEmail = (EditText) findViewById(R.id.loginUsername);

        Intent intent = new Intent(this, ForgotPasswordACT.class);
        intent.putExtra(getString(R.string.username), ETEmail.getText().toString());
        startActivity(intent);
    }


}
