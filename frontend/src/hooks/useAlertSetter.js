import { useState } from "react";

function useAlertSetter() {
    const [alert, setAlert] = useState({
        visible: false,
        severity: "",
        message: "",
    });

    const showAlert = (severity, message) => {
        setAlert({ visible: true, severity: severity, message: message });
    };

    const hideAlert = () => {
        setAlert({ visible: false, severity: "", message: "" });
    };

    return { alert, showAlert, hideAlert };
}

export default useAlertSetter;