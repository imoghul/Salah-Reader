package com.example.salahreader;

import android.database.DataSetObserver;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
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
    public SettingsFragment sf;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        sf = new SettingsFragment();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settings_activity);

        if (savedInstanceState == null) {
            getSupportFragmentManager()
            .beginTransaction()
            .replace(R.id.settings, sf)
            .commit();
        }



        ActionBar actionBar = getSupportActionBar();

        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(false);
            actionBar.setDisplayShowHomeEnabled(true);
        }

    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.options_menu, menu);
        return true;
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        switch(id){
            case R.id.refreshButton:
                RetrieveAPI.refresh();
                if(sf!=null) sf.updateTimes();
                break;
            default:
                break;
        }
        return super.onOptionsItemSelected(item);
    }

    public static class SettingsFragment extends PreferenceFragmentCompat {
        @RequiresApi(api = Build.VERSION_CODES.O)
        @Override
        public void onCreatePreferences(Bundle savedInstanceState, String rootKey) {
            setPreferencesFromResource(R.xml.root_preferences, rootKey);
            // update and retrive values from API
            RetrieveAPI.refresh();
            // update text prefernces
            updateTimes();
        }

        public void updateTimesTextView(){
            String[] todaysTimes = RetrieveAPI.getCurrentTimes();
            EditTextPreference myTextView;
            String[] keys = {"fajrTime","thuhrTime","asrTime","magribTime","ishaaTime"};
            for(int i = 0;i<5;++i){
                myTextView = (EditTextPreference) findPreference(keys[i]);
                myTextView.setTitle(todaysTimes[i]);
                myTextView.setText(todaysTimes[i]);
                myTextView.setEnabled(false);
            }
        }
        public void updateTimes(){
            updateTimesTextView();
        }
    }
}

