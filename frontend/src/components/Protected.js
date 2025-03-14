import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = ({ element: Element, ...rest }) => {
    const token = localStorage.getItem("token");

    // If there is no token or the token is expired, redirect to login
    if (!token) {
        return <Navigate to="/login" replace />;
    }

    return <Element {...rest} />;
};


export default ProtectedRoute;
