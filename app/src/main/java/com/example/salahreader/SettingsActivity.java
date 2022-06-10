package com.example.salahreader;

import android.database.DataSetObserver;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.SpinnerAdapter;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.EditTextPreference;
import androidx.preference.PreferenceFragmentCompat;

public class SettingsActivity extends AppCompatActivity {
    ArrayAdapter<String> adapter;
    public final String[] DropdownOptions = {"Refresh"};
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

        adapter = new ArrayAdapter<String>(this, android.R.layout.simple_expandable_list_item_1, DropdownOptions);

        ActionBar actionBar = getSupportActionBar();

        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(false);
            actionBar.setDisplayShowHomeEnabled(true);
        }
        
    }

    public static class SettingsFragment extends PreferenceFragmentCompat {
        @RequiresApi(api = Build.VERSION_CODES.O)
        @Override
        public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
            setPreferencesFromResource(R.xml.root_preferences, rootKey);
            // update and retrive values from API
            RetrieveAPI.refresh();
            String[] todaysTimes = RetrieveAPI.getCurrentTimes();
            // update text prefernces
            EditTextPreference myTextView;
            String[] keys = {"fajrTime","thuhrTime","asrTime","magribTime","ishaaTime"};
            for(int i = 0;i<5;++i){
                myTextView = (EditTextPreference) findPreference(keys[i]);
                myTextView.setTitle(todaysTimes[i]);
                myTextView.setText(todaysTimes[i]);
                myTextView.setEnabled(false);
            }
        }
    }
}

