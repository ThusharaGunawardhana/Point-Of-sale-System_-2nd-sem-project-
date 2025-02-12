import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class LoginGUI extends JFrame implements ActionListener {
    private JTextField usernameField;
    private JPasswordField passwordField;
    private Connection connection;

    public LoginGUI() {
        setTitle("Herath Accessories");
        setSize(500, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(null);

        JLabel usernameLabel = new JLabel("Username");
        usernameLabel.setBounds(100, 200, 80, 30);
        add(usernameLabel);

        JLabel passwordLabel = new JLabel("Password");
        passwordLabel.setBounds(100, 250, 80, 30);
        add(passwordLabel);

        usernameField = new JTextField();
        usernameField.setBounds(200, 200, 150, 30);
        add(usernameField);

        passwordField = new JPasswordField();
        passwordField.setBounds(200, 250, 150, 30);
        add(passwordField);

        JButton loginButton = new JButton(new ImageIcon("login_button.png"));
        loginButton.setBounds(210, 300, 80, 40);
        loginButton.addActionListener(this);
        add(loginButton);

        JButton createAccButton = new JButton(new ImageIcon("createacc.png"));
        createAccButton.setBounds(198, 350, 100, 40);
        createAccButton.addActionListener(e -> {
            dispose(); // Close the current login window
            new CreateAccountGUI(); // Open the create account window
        });
        add(createAccButton);

        try {
            connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/2nd", "root", "");
        } catch (SQLException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Failed to connect to the database.");
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getActionCommand().equals("login")) {
            String username = usernameField.getText();
            String password = new String(passwordField.getPassword());

            if (username.isEmpty() || password.isEmpty()) {
                JOptionPane.showMessageDialog(null, "Username and password cannot be blank.");
                return;
            }

            try {
                PreparedStatement statement = connection.prepareStatement("SELECT * FROM employee WHERE email = ? AND password = ?");
                statement.setString(1, username);
                statement.setString(2, password);
                ResultSet resultSet = statement.executeQuery();

                if (resultSet.next()) {
                    JOptionPane.showMessageDialog(null, "Employee Login Success");
                    dispose(); // Close login window
                    // Open POS 2 GUI
                    // Example: new POS2GUI();
                } else if (username.equals("admin") && password.equals("87654321")) {
                    JOptionPane.showMessageDialog(null, "Admin Login Success");
                    dispose(); // Close login window
                    // Open another GUI for admin
                    // Example: new AdminGUI();
                } else {
                    JOptionPane.showMessageDialog(null, "Invalid username or password.");
                }
            } catch (SQLException ex) {
                ex.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        // Load MySQL JDBC driver
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Failed to load MySQL JDBC driver.");
            return;
        }

        // Create and display the login GUI
        SwingUtilities.invokeLater(() -> new LoginGUI().setVisible(true));
    }
}
