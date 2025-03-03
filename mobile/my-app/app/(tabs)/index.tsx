import { View, TextInput, TouchableOpacity, Text, StyleSheet } from "react-native";
import React, { useState } from "react";
import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

const URL = "http://127.0.0.1:8000";//"https://DOMAIN";

export default function HomeScreen() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const res = await fetch(`${URL}/items/1?q=${encodeURIComponent(query)}`);
      if (!res.ok) {
        setResponse(`${res.status}`);
        return;
      }
      const data = await res.json();
      setResponse(`200 Ok: ${JSON.stringify(data, null, 2)}`);
    } catch (error) {
      setResponse(`Network Error ${error}`);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.inputContainer}>
        <TextInput
          placeholder="Enter request"
          value={query}
          onChangeText={setQuery}
          style={styles.input}
        />
        <TouchableOpacity onPress={fetchData} style={styles.button}>
          <Text style={styles.buttonText}>Make request</Text>
        </TouchableOpacity>
      </View>
      {response && (
        <Text style={styles.responseBox}>{response}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
    flex: 1,
    justifyContent: 'center', // Center content vertically
    alignItems: 'center', // Center content horizontally
    backgroundColor: '#fff', // Match web's background
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    borderRadius: 5,
    width: 200,
  },
  button: {
    backgroundColor: '#007bff',
    padding: 10,
    borderRadius: 5,
  },
  buttonText: {
    color: 'white',
  },
  responseBox: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    width: 250,
    textAlign: 'center',
    backgroundColor: '#f9f9f9',
  },
});
