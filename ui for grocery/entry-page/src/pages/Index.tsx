import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect } from "react";
import heroImage from "../assets/hero-groceries.jpg";
import { ArrowRight } from "lucide-react";

const floatingItems = ["🍎", "🥑", "🍋", "🥕", "🍇", "🌽", "🍊", "🥦", "🍓", "🫐"];

const Index = () => {
  const [loaded, setLoaded] = useState(false);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    const t1 = setTimeout(() => setLoaded(true), 300);
    const t2 = setTimeout(() => setShowContent(true), 1200);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, []);

  return (
    <div className="relative min-h-screen bg-background overflow-hidden flex items-center justify-center">
      {/* Ambient glow effects */}
      <div className="absolute inset-0 pointer-events-none">
        <motion.div
          animate={{ scale: [1, 1.2, 1], opacity: [0.15, 0.25, 0.15] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-[-20%] left-[-10%] w-[60vw] h-[60vw] rounded-full blur-[120px]"
          style={{ background: "hsl(155 65% 42% / 0.2)" }}
        />
        <motion.div
          animate={{ scale: [1.1, 1, 1.1], opacity: [0.1, 0.2, 0.1] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
          className="absolute bottom-[-20%] right-[-10%] w-[50vw] h-[50vw] rounded-full blur-[100px]"
          style={{ background: "hsl(30 75% 55% / 0.15)" }}
        />
      </div>

      {/* Floating emoji particles */}
      {floatingItems.map((emoji, i) => (
        <motion.span
          key={i}
          className="absolute text-3xl md:text-4xl select-none pointer-events-none"
          initial={{
            opacity: 0,
            x: `${10 + (i % 5) * 20}vw`,
            y: `${15 + Math.floor(i / 5) * 50}vh`,
          }}
          animate={{
            opacity: [0, 0.6, 0],
            y: [`${15 + Math.floor(i / 5) * 50}vh`, `${5 + Math.floor(i / 5) * 50}vh`],
            rotate: [0, i % 2 === 0 ? 20 : -20, 0],
          }}
          transition={{
            duration: 5 + i * 0.5,
            repeat: Infinity,
            delay: 1.5 + i * 0.3,
            ease: "easeInOut",
          }}
        >
          {emoji}
        </motion.span>
      ))}

      {/* Background image with parallax */}
      <motion.div
        className="absolute inset-0"
        initial={{ scale: 1.2, opacity: 0 }}
        animate={{ scale: 1, opacity: 0.15 }}
        transition={{ duration: 2, ease: "easeOut" }}
      >
        <img src={heroImage} alt="" className="w-full h-full object-cover" />
      </motion.div>

      {/* Grain overlay */}
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{ backgroundImage: "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E\")" }}
      />

      {/* Main content */}
      <div className="relative z-10 text-center px-6 max-w-3xl mx-auto">
        {/* Logo reveal */}
        <AnimatePresence>
          {loaded && (
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0 }}
              className="mb-8"
            >
              <span className="text-7xl md:text-8xl block drop-shadow-2xl">🥬</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Store name */}
        <AnimatePresence>
          {loaded && (
            <motion.h1
              initial={{ opacity: 0, y: 50, filter: "blur(10px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              transition={{ duration: 0.8, delay: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="text-5xl md:text-8xl font-display font-black tracking-tight text-foreground leading-none"
            >
              Arya
              <span className="text-primary">FoodMart</span>
            </motion.h1>
          )}
        </AnimatePresence>

        {/* Tagline */}
        <AnimatePresence>
          {loaded && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.8 }}
              className="mt-6 mb-10"
            >
              <div className="inline-flex items-center gap-3 px-5 py-2 rounded-full border border-border bg-card/50 backdrop-blur-sm">
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                <span className="text-sm md:text-base font-body font-medium text-muted-foreground tracking-wide">
                  Farm-fresh groceries, delivered daily
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Subtitle */}
        <AnimatePresence>
          {showContent && (
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-lg md:text-xl text-muted-foreground font-body max-w-md mx-auto leading-relaxed mb-12"
            >
              Welcome! Explore handpicked organic produce and artisan goods from local farmers.
            </motion.p>
          )}
        </AnimatePresence>

        {/* CTA Button */}
        <AnimatePresence>
          {showContent && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 20, delay: 0.3 }}
            >
              <motion.a
                href="/store"
                whileHover={{ scale: 1.05, boxShadow: "0 0 40px hsl(155 65% 42% / 0.4)" }}
                whileTap={{ scale: 0.97 }}
                className="inline-flex items-center gap-3 px-10 py-5 rounded-full bg-primary text-primary-foreground font-body font-bold text-lg transition-colors hover:bg-primary/90 cursor-pointer"
              >
                Explore Store
                <motion.span
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                >
                  <ArrowRight className="w-5 h-5" />
                </motion.span>
              </motion.a>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Bottom decorative line */}
        <AnimatePresence>
          {showContent && (
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ duration: 1, delay: 0.6, ease: [0.22, 1, 0.36, 1] }}
              className="mt-16 mx-auto w-32 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent"
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Index;
