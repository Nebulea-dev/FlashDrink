import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert, TextInput } from 'react-native';
import NfcManager, { NfcTech } from 'react-native-nfc-manager';
import { BACKEND_URL } from '../constants/backend';

interface ScanScreenProps {
  userId: number;
}

const ScanScreen: React.FC<ScanScreenProps> = ({ userId }) => {
  const [balance, setBalance] = useState<number | null>(null);
  const [amount, setAmount] = useState<string>(''); // Input for amount to add
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isScanning, setIsScanning] = useState<boolean>(false); // New state for scanning
  const [connectedTag, setConnectedTag] = useState<string | null>(null); // Track connected tag ID

  // Function to fetch balance from the backend
  const fetchBalance = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}getBalance?user_id=${userId}`);
      const data = await response.json();
      if (data.balance !== undefined) {
        setBalance(data.balance);
      } else {
        Alert.alert('Error', 'Unable to fetch balance');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to fetch balance');
    }
  };

  // Function to add balance
  const addBalance = async () => {
    if (!amount || isNaN(Number(amount)) || Number(amount) <= 0) {
      Alert.alert('Error', 'Please enter a valid amount');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}addBalance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          amount: Number(amount),
        }),
      });
      const data = await response.json();
      if (data.message) {
        Alert.alert('Success', data.message);
        setAmount(''); // Clear the input field
        fetchBalance(); // Refresh balance
      } else {
        Alert.alert('Error', data.error || 'Failed to add balance');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to add balance');
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle NFC scanning and connecting the tag
  const readNdef = async () => {
    setIsScanning(true); // Enable scanning state
    try {
      await NfcManager.requestTechnology(NfcTech.Ndef);
      const tag = await NfcManager.getTag();
      const tagId = tag.id;

      if (!tagId) {
        Alert.alert('Error', 'Invalid tag ID');
        return;
      }

      const response = await fetch(`${BACKEND_URL}connectTagWithUser`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tag_id: tagId, user_id: userId }),
      });
      const data = await response.json();

      if (data.message) {
        Alert.alert('Success', 'Tag connected successfully');
        setConnectedTag(tagId); // Update the connected tag ID
      } else {
        Alert.alert('Error', data.error || 'Failed to connect tag');
      }
    } catch (ex) {
      Alert.alert('Error', 'Failed to scan tag');
    } finally {
      setIsScanning(false); // Reset scanning state
      NfcManager.cancelTechnologyRequest();
    }
  };

  // Function to disconnect the tag
  const disconnectTag = async () => {
    if (!connectedTag) return;

    try {
      const response = await fetch(`${BACKEND_URL}disconnectTag`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tag_id: connectedTag }),
      });
      const data = await response.json();

      if (data.message) {
        Alert.alert('Success', 'Tag disconnected successfully');
        setConnectedTag(null); // Clear the connected tag ID
      } else {
        Alert.alert('Error', data.error || 'Failed to disconnect tag');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to disconnect tag');
    }
  };

  // Fetch balance when the screen is loaded
  useEffect(() => {
    fetchBalance();
  }, []);

  return (
    <View style={styles.wrapper}>
      <Text style={styles.title}>Scan RFID Tag</Text>

      <TouchableOpacity
        style={[styles.button, connectedTag ? styles.disconnectButton : null]}
        onPress={connectedTag ? disconnectTag : readNdef}
        disabled={isScanning} // Disable during scanning or if a tag is connected
      >
        <Text style={styles.buttonText}>
          {connectedTag ? 'Disconnect Tag' : isScanning ? 'Scanning...' : 'Scan a Tag'}
        </Text>
      </TouchableOpacity>

      {balance !== null && (
        <>
          <Text style={styles.balanceText}>Current Balance: ${balance}</Text>

          <TextInput
            style={styles.input}
            value={amount}
            onChangeText={setAmount}
            keyboardType="numeric"
            placeholder="Enter amount to add"
          />

          <TouchableOpacity style={styles.button} onPress={addBalance} disabled={isLoading}>
            <Text style={styles.buttonText}>{isLoading ? 'Adding...' : 'Add Balance'}</Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f9f9f9',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#333',
  },
  balanceText: {
    fontSize: 18,
    marginVertical: 10,
    color: '#333',
  },
  button: {
    backgroundColor: '#007BFF',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
    marginBottom: 10,
  },
  disconnectButton: {
    backgroundColor: '#FF0000', // Red background for the "Disconnect" button
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  input: {
    height: 40,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 10,
    width: '100%',
    marginVertical: 10,
  },
});

export default ScanScreen;

