package com.example.salahreader;

import android.os.Build;
import android.os.Build;
import android.os.Bundle;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.EditTextPreference;
import androidx.preference.PreferenceFragmentCompat;
import androidx.annotation.RequiresApi;
import androidx.preference.EditTextPreference;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.format.TextStyle;
import java.util.Locale;
import java.util.Map;

public class RetrieveAPI {
    private static String[] currentTimes;

    @RequiresApi(api = Build.VERSION_CODES.O)
    public static void refresh() {
        GetData g = new GetData();
        Thread thread = new Thread(g);
        thread.start();

        String d;

        while((d =  g.getValue()).equals(""));

        Map<String, String[]> data = GetSalah.parser(d);

        LocalDate date = LocalDate.now();
        DayOfWeek dow = date.getDayOfWeek();
        String dayName = dow.getDisplayName(TextStyle.FULL_STANDALONE, Locale.ENGLISH);
        RetrieveAPI.currentTimes = data.get(dayName);

    }

    public static String[] getCurrentTimes(){
        return RetrieveAPI.currentTimes;
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
