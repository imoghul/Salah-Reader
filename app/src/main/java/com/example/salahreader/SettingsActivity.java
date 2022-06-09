package com.example.salahreader;

import android.os.Build;
import android.os.Bundle;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.EditTextPreference;
import androidx.preference.PreferenceFragmentCompat;

import java.io.FileOutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.format.TextStyle;
import java.util.Calendar;
import java.util.Locale;
import java.util.Map;
import java.util.HashMap;

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
        @RequiresApi(api = Build.VERSION_CODES.O)
        @Override
        public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
            setPreferencesFromResource(R.xml.root_preferences, rootKey);

            GetData g = new GetData();
            Thread thread = new Thread(g);
            thread.start();

            String d;
            while((d =  g.getValue()).equals(""));
            Map<String, String[]> data = GetSalah.parser(d);

            LocalDate date = LocalDate.now();
            DayOfWeek dow = date.getDayOfWeek();
            String dayName = dow.getDisplayName(TextStyle.FULL_STANDALONE, Locale.ENGLISH);
            String[] todaysTimes = data.get(dayName);
            //Place after here
            EditTextPreference[] myTextView = new EditTextPreference[5];
            myTextView[0] = (EditTextPreference) findPreference("fajrTime");
            myTextView[0].setTitle(todaysTimes[0]);
            myTextView[0].setEnabled(false);
            myTextView[1] = (EditTextPreference) findPreference("thuhrTime");
            myTextView[1].setTitle(todaysTimes[1]);
            myTextView[1].setEnabled(false);
            myTextView[2] = (EditTextPreference) findPreference("asrTime");
            myTextView[2].setTitle(todaysTimes[2]);
            myTextView[2].setEnabled(false);
            myTextView[3] = (EditTextPreference) findPreference("magribTime");
            myTextView[3].setTitle(todaysTimes[3]);
            myTextView[3].setEnabled(false);
            myTextView[4] = (EditTextPreference) findPreference("ishaaTime");
            myTextView[4].setTitle(todaysTimes[4]);
            myTextView[4].setEnabled(false);
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