import React, { useState } from 'react';
import { UserContext } from './contexts/UserContext';
import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';
import ScanScreen from './screens/ScanScreen';

const App: React.FC = () => {
  const [userId, setUserId] = useState<number | null>(null);
  const [isRegistering, setIsRegistering] = useState<boolean>(false);

  if (userId) {
    return <ScanScreen userId={userId} />;
  }

  return isRegistering ? (
    <RegisterScreen onNavigateToLogin={() => setIsRegistering(false)} />
  ) : (
    <LoginScreen
      onLoginSuccess={setUserId}
      onNavigateToRegister={() => setIsRegistering(true)}
    />
  );
};

export default App;

