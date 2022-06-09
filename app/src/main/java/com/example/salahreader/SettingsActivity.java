package com.example.salahreader;

import android.os.Bundle;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.EditTextPreference;
import androidx.preference.PreferenceFragmentCompat;

import java.io.FileOutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;

public class SettingsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settings_activity);

        if (savedInstanceState == null) {
            getSupportFragmentManager()
            .beginTransaction()
            .replace(R.id.settings, new SettingsFragment())
            .commit();
        }

        ActionBar actionBar = getSupportActionBar();

        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(true);
        }
    }

    public static class SettingsFragment extends PreferenceFragmentCompat {
        @Override
        public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
            setPreferencesFromResource(R.xml.root_preferences, rootKey);
            GetData g = new GetData();
            Thread thread = new Thread(g);
            thread.start();
//            thread.join();
            String d = g.getValue();
//            // Load the preferences from an XML resource
//            addPreferencesFromResource(R.xml.root_preferences);
//            //Place after here
//            EditTextPreference[] myTextView = new EditTextPreference[10];
//            myTextView[0] = (EditTextPreference) findPreference("fajrTime");
//            myTextView[0].setTitle(data);
        }
    }
}

class GetData implements Runnable {
    private volatile String value = "";

    @Override
    public void run() {
        value = GetSalah.getDataStr();
    }

    public String getValue() {
        return value;
    }
}