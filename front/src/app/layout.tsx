import "./globals.css";
import { ReactNode } from "react";
import { ToastContainer } from "react-toastify";

interface AppProps {
  children: ReactNode;
}

export const metadata = {
  title: "Youtube mp3",
  description: "Solve Youtube mp3 to unlock the next clue!",
};

export default function App({ children }: AppProps) {

  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 relative">
      <nav className="p-4 bg-white border-b shadow-md sticky top-0 z-30 flex justify-between items-center">
        <div className="text-xl font-bold text-red-600 tracking-wide">
          <a href="/" className="transition-colors">
            Youtube mp3
          </a>
        </div>

      </nav>
        <main className="min-h-[85vh] p-4">{children}</main>
        <footer className="p-4 text-center border-t text-sm text-gray-500">
          {/* https://github.com/BEQSONA-cmd */}
          <p>
            Made with ❤️ by{" "}
            <a
              href="https://github.com/BEQSONA-cmd"
              className="text-red-600 hover:underline"
            >
              BEQSONA-cmd
            </a>
          </p>
        </footer>
        <ToastContainer />
      </body>
    </html>
  );
}