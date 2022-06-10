package com.example.salahreader;

import android.os.Build;
import android.os.Bundle;

import androidx.annotation.RequiresApi;
import androidx.preference.EditTextPreference;
import androidx.preference.PreferenceFragmentCompat;

public class SettingsFragment extends PreferenceFragmentCompat {
    private boolean state = false;
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
        // retrieve times data for today
        String[] todaysTimes = RetrieveAPI.getCurrentTimes();
        // update text views
        EditTextPreference myTextView;
        String[] keys = {"fajrTime","thuhrTime","asrTime","magribTime","ishaaTime"};
        state=!state;
        for(int i = 0;i<5;++i){
            myTextView = (EditTextPreference) findPreference(keys[i]);
            myTextView.setTitle(todaysTimes[i]);
            myTextView.setText(todaysTimes[i]);
            myTextView.setEnabled(state);
        }
    }
    public void updateTimes(){
        updateTimesTextView();
        // TODO: create alarms
    }
}