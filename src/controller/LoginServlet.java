package controller;

import dao.UserDAO;
import model.User;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    private final UserDAO userDAO = new UserDAO();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        String email = request.getParameter("email");
        String password = request.getParameter("password");

        if (username == null || username.trim().length() < 3 || email == null || !email.matches("^[a-zA-Z0-9._%+-]+@gmail\\.com$") || password == null || password.length() < 6) {
            response.sendRedirect("index.jsp");
            return;
        }

        User existingUser = userDAO.findByEmail(email);
        User currentUser;
        if (existingUser != null) {
            if (!existingUser.getPassword().equals(password)) {
                response.sendRedirect("index.jsp");
                return;
            }
            currentUser = existingUser;
        } else {
            currentUser = new User(username.trim(), email.trim(), password);
            boolean created = userDAO.createUser(currentUser);
            if (!created) {
                response.sendRedirect("index.jsp");
                return;
            }
        }

        HttpSession session = request.getSession();
        session.setAttribute("userId", currentUser.getId());
        session.setAttribute("username", currentUser.getUsername());
        session.setAttribute("email", currentUser.getEmail());
        session.setMaxInactiveInterval(30 * 60);

        response.sendRedirect("dashboard.jsp");
    }
}
