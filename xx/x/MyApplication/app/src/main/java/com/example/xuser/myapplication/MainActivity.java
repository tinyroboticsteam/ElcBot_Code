package com.example.xuser.myapplication;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.OutputStreamWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.ClassNotFoundException;
import java.net.ServerSocket;
import java.net.Socket;
import android.util.Log;

import android.app.Activity;
import android.app.IntentService;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;


public class MainActivity extends AppCompatActivity {
    static final String TAG = "AndroidCheatSocket";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(MainActivity.TAG, "onCreate");
        MainActivity.this.startService(new Intent(MainActivity.this, MyService.class));
    }

    /*python:::
    * import socket
sock = socket.socket()
sock.connect(('192.168.0.105', 12345))
sock.send(b'Mama!')
sock.close()
    *
    * */

    public static class MyService extends IntentService {
        public MyService() {
            super("MyService");
        }
        @Override
        protected void onHandleIntent(Intent intent) {
            Log.d(MainActivity.TAG, "onHandleIntent");
            final int port = 12345;
            ServerSocket listener = null;
            try {
                listener = new ServerSocket(port);
                Log.d(MainActivity.TAG, String.format("listening on port = %d", port));
                while (true) {
                    Log.d(MainActivity.TAG, "waiting for client");
                    Socket socket = listener.accept();
                    Log.d(MainActivity.TAG, String.format("client connected from: %s", socket.getRemoteSocketAddress().toString()));
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    PrintStream out = new PrintStream(socket.getOutputStream());
                    for (String inputLine; (inputLine = in.readLine()) != null;) {
                        Log.d(MainActivity.TAG, "received");
                        Log.d(MainActivity.TAG, inputLine);
                        StringBuilder outputStringBuilder = new StringBuilder("");
                        char inputLineChars[] = inputLine.toCharArray();
                        for (char c : inputLineChars)
                            outputStringBuilder.append(Character.toChars(c + 1));
                        out.println(outputStringBuilder);
                    }
                }
            } catch(IOException e) {
                Log.d(MainActivity.TAG, e.toString());
            }
        }
    }
}
