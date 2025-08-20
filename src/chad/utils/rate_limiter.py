#!/usr/bin/env python3

"""
Advanced Rate Limiting and Performance Manager for Enhanced Chad
Provides intelligent rate limiting, performance monitoring, and optimization
"""

import time
import random
import statistics
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading

@dataclass
class QueryMetrics:
    """Metrics for individual queries"""
    query: str
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = False
    error_type: Optional[str] = None
    response_time: float = 0.0
    results_count: int = 0
    ip_used: str = ""
    user_agent_used: str = ""

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    # Basic timing
    min_query_delay: float = 75.0     # Minimum delay between queries (seconds)
    max_query_delay: float = 125.0    # Maximum delay between queries
    min_page_delay: float = 15.0      # Minimum delay between pages
    max_page_delay: float = 25.0      # Maximum delay between pages
    
    # Adaptive timing
    enable_adaptive: bool = True      # Enable adaptive rate limiting
    success_speedup: float = 0.9      # Multiply delay by this on success
    error_slowdown: float = 1.5       # Multiply delay by this on error
    min_speedup_delay: float = 30.0   # Minimum delay even with speedup
    max_slowdown_delay: float = 300.0 # Maximum delay even with slowdown
    
    # Rate limit detection
    rate_limit_keywords: List[str] = field(default_factory=lambda: [
        "rate limit", "too many requests", "429", "blocked",
        "suspicious traffic", "automated", "robot", "captcha"
    ])
    
    # IP rotation triggers
    ip_rotation_on_error: bool = True    # Rotate IP on rate limit
    ip_rotation_interval: int = 10       # Rotate IP every N queries
    ip_rotation_on_failure_count: int = 3 # Rotate IP after N consecutive failures
    
    # Performance thresholds
    slow_response_threshold: float = 30.0  # Consider response slow if > 30s
    success_rate_threshold: float = 0.8    # Consider performance bad if success rate < 80%

class AdvancedRateLimiter:
    """Advanced rate limiting with adaptive behavior and performance monitoring"""
    
    def __init__(self, config: Optional[RateLimitConfig] = None, tor_manager=None):
        self.config = config or RateLimitConfig()
        self.tor_manager = tor_manager
        
        # Performance tracking
        self.query_metrics: List[QueryMetrics] = []
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.current_query_delay = self.config.min_query_delay
        self.current_page_delay = self.config.min_page_delay
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Statistics
        self.total_queries = 0
        self.successful_queries = 0
        self.total_response_time = 0.0
        self.ip_rotations = 0
        
        print(f"[+] Advanced Rate Limiter initialized")
        print(f"    Base query delay: {self.config.min_query_delay}-{self.config.max_query_delay}s")
        print(f"    Adaptive rate limiting: {'Enabled' if self.config.enable_adaptive else 'Disabled'}")
        print(f"    IP rotation: Every {self.config.ip_rotation_interval} queries")
    
    def start_query(self, query: str) -> QueryMetrics:
        """Start tracking a new query"""
        with self.lock:
            self.total_queries += 1
            
            # Check if IP rotation is needed
            if self._should_rotate_ip():
                self._rotate_ip()
            
            # Create metrics
            metrics = QueryMetrics(
                query=query,
                start_time=datetime.now(),
                ip_used=self._get_current_ip(),
                user_agent_used=self._get_current_user_agent()
            )
            
            return metrics
    
    def end_query(self, metrics: QueryMetrics, success: bool, 
                  error_type: Optional[str] = None, results_count: int = 0) -> None:
        """End query tracking and update metrics"""
        with self.lock:
            metrics.end_time = datetime.now()
            metrics.success = success
            metrics.error_type = error_type
            metrics.results_count = results_count
            metrics.response_time = (metrics.end_time - metrics.start_time).total_seconds()
            
            self.query_metrics.append(metrics)
            
            # Update counters
            if success:
                self.successful_queries += 1
                self.consecutive_successes += 1
                self.consecutive_failures = 0
            else:
                self.consecutive_successes = 0
                self.consecutive_failures += 1
            
            self.total_response_time += metrics.response_time
            
            # Adaptive rate limiting
            if self.config.enable_adaptive:
                self._update_adaptive_delays(success, error_type)
            
            # Print status
            self._print_query_status(metrics)
    
    def wait_between_queries(self) -> None:
        """Wait appropriate time between queries"""
        delay = self._calculate_query_delay()
        print(f"[*] Waiting {delay:.1f}s between queries (adaptive: {self.config.enable_adaptive})")
        time.sleep(delay)
    
    def wait_between_pages(self) -> None:
        """Wait appropriate time between pages"""
        delay = self._calculate_page_delay()
        print(f"[*] Waiting {delay:.1f}s between pages")
        time.sleep(delay)
    
    def _should_rotate_ip(self) -> bool:
        """Determine if IP should be rotated"""
        if not self.tor_manager:
            return False
        
        # Rotate on interval
        if self.total_queries > 0 and self.total_queries % self.config.ip_rotation_interval == 0:
            print(f"[*] IP rotation triggered by interval ({self.config.ip_rotation_interval} queries)")
            return True
        
        # Rotate on consecutive failures
        if (self.config.ip_rotation_on_failure_count > 0 and 
            self.consecutive_failures >= self.config.ip_rotation_on_failure_count):
            print(f"[*] IP rotation triggered by {self.consecutive_failures} consecutive failures")
            return True
        
        return False
    
    def _rotate_ip(self) -> None:
        """Rotate IP using Tor manager"""
        if self.tor_manager:
            print(f"[*] Rotating IP address...")
            if self.tor_manager.rotate_ip():
                self.ip_rotations += 1
                # Add extra delay after IP rotation
                extra_delay = random.uniform(30, 60)
                print(f"[*] IP rotated successfully, waiting {extra_delay:.1f}s for stabilization")
                time.sleep(extra_delay)
            else:
                print(f"[!] IP rotation failed")
    
    def _update_adaptive_delays(self, success: bool, error_type: Optional[str] = None) -> None:
        """Update delays based on success/failure patterns"""
        if success:
            # Speed up on success
            self.current_query_delay *= self.config.success_speedup
            self.current_query_delay = max(self.current_query_delay, self.config.min_speedup_delay)
            
            self.current_page_delay *= self.config.success_speedup
            self.current_page_delay = max(self.current_page_delay, 
                                        self.config.min_page_delay * self.config.success_speedup)
        else:
            # Slow down on error
            if self._is_rate_limit_error(error_type):
                # Extra slowdown for rate limits
                multiplier = self.config.error_slowdown * 1.5
            else:
                multiplier = self.config.error_slowdown
            
            self.current_query_delay *= multiplier
            self.current_query_delay = min(self.current_query_delay, self.config.max_slowdown_delay)
            
            self.current_page_delay *= multiplier
            self.current_page_delay = min(self.current_page_delay, 
                                        self.config.max_page_delay * multiplier)
    
    def _is_rate_limit_error(self, error_type: Optional[str] = None) -> bool:
        """Check if error indicates rate limiting"""
        if not error_type:
            return False
        
        error_lower = error_type.lower()
        return any(keyword in error_lower for keyword in self.config.rate_limit_keywords)
    
    def _calculate_query_delay(self) -> float:
        """Calculate delay between queries"""
        if self.config.enable_adaptive:
            base_delay = self.current_query_delay
        else:
            base_delay = random.uniform(self.config.min_query_delay, self.config.max_query_delay)
        
        # Add random variation
        variation = base_delay * 0.1  # 10% variation
        return base_delay + random.uniform(-variation, variation)
    
    def _calculate_page_delay(self) -> float:
        """Calculate delay between pages"""
        if self.config.enable_adaptive:
            base_delay = self.current_page_delay
        else:
            base_delay = random.uniform(self.config.min_page_delay, self.config.max_page_delay)
        
        # Add random variation
        variation = base_delay * 0.1  # 10% variation
        return base_delay + random.uniform(-variation, variation)
    
    def _get_current_ip(self) -> str:
        """Get current IP address"""
        if self.tor_manager:
            return self.tor_manager.current_ip or "Unknown"
        return "Direct"
    
    def _get_current_user_agent(self) -> str:
        """Get current user agent"""
        if self.tor_manager:
            ua = self.tor_manager.get_random_user_agent()
            return ua[:50] + "..." if len(ua) > 50 else ua
        return "Default"
    
    def _print_query_status(self, metrics: QueryMetrics) -> None:
        """Print query status information"""
        status = "✅" if metrics.success else "❌"
        
        print(f"{status} Query: {metrics.query[:50]}...")
        print(f"    Response time: {metrics.response_time:.1f}s")
        print(f"    Results: {metrics.results_count}")
        print(f"    IP: {metrics.ip_used}")
        
        if not metrics.success and metrics.error_type:
            print(f"    Error: {metrics.error_type}")
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        with self.lock:
            if not self.query_metrics:
                return {"status": "No data available"}
            
            success_rate = self.successful_queries / self.total_queries if self.total_queries > 0 else 0
            avg_response_time = self.total_response_time / self.total_queries if self.total_queries > 0 else 0
            
            response_times = [m.response_time for m in self.query_metrics if m.response_time > 0]
            
            stats = {
                "total_queries": self.total_queries,
                "successful_queries": self.successful_queries,
                "success_rate": f"{success_rate:.2%}",
                "average_response_time": f"{avg_response_time:.1f}s",
                "ip_rotations": self.ip_rotations,
                "consecutive_failures": self.consecutive_failures,
                "consecutive_successes": self.consecutive_successes,
                "current_query_delay": f"{self.current_query_delay:.1f}s",
                "current_page_delay": f"{self.current_page_delay:.1f}s"
            }
            
            if response_times:
                stats.update({
                    "median_response_time": f"{statistics.median(response_times):.1f}s",
                    "fastest_response": f"{min(response_times):.1f}s",
                    "slowest_response": f"{max(response_times):.1f}s"
                })
            
            return stats
    
    def print_performance_report(self) -> None:
        """Print detailed performance report"""
        stats = self.get_performance_stats()
        
        print("\n" + "="*60)
        print("📊 PERFORMANCE REPORT")
        print("="*60)
        
        for key, value in stats.items():
            if key == "status":
                print(f"{value}")
            else:
                formatted_key = key.replace("_", " ").title()
                print(f"{formatted_key:.<30} {value}")
        
        # Performance assessment
        if "success_rate" in stats:
            success_rate = self.successful_queries / self.total_queries
            if success_rate >= self.config.success_rate_threshold:
                print("\n🎯 Performance: EXCELLENT")
            elif success_rate >= 0.6:
                print("\n⚠️  Performance: MODERATE - Consider adjusting delays")
            else:
                print("\n🚨 Performance: POOR - Rate limiting detected")
                print("   Recommendations:")
                print("   • Increase delays between queries")
                print("   • Enable IP rotation")
                print("   • Use different user agents")
        
        print("="*60)
    
    def export_metrics(self, filename: str) -> None:
        """Export metrics to JSON file"""
        import json
        
        with self.lock:
            # Calculate stats directly to avoid recursive locking
            if not self.query_metrics:
                stats = {"status": "No data available"}
            else:
                success_rate = self.successful_queries / self.total_queries if self.total_queries > 0 else 0
                avg_response_time = self.total_response_time / self.total_queries if self.total_queries > 0 else 0
                response_times = [m.response_time for m in self.query_metrics if m.response_time > 0]
                
                stats = {
                    "total_queries": self.total_queries,
                    "successful_queries": self.successful_queries,
                    "success_rate": f"{success_rate:.2%}",
                    "average_response_time": f"{avg_response_time:.1f}s",
                    "ip_rotations": self.ip_rotations,
                    "consecutive_failures": self.consecutive_failures,
                    "consecutive_successes": self.consecutive_successes,
                    "current_query_delay": f"{self.current_query_delay:.1f}s",
                    "current_page_delay": f"{self.current_page_delay:.1f}s",
                    "median_response_time": f"{statistics.median(response_times):.1f}s" if response_times else "0.0s",
                    "fastest_response": f"{min(response_times):.1f}s" if response_times else "0.0s",
                    "slowest_response": f"{max(response_times):.1f}s" if response_times else "0.0s"
                }
            
            data = {
                "config": {
                    "min_query_delay": self.config.min_query_delay,
                    "max_query_delay": self.config.max_query_delay,
                    "adaptive_enabled": self.config.enable_adaptive,
                    "ip_rotation_interval": self.config.ip_rotation_interval
                },
                "statistics": stats,
                "queries": [
                    {
                        "query": m.query,
                        "start_time": m.start_time.isoformat(),
                        "end_time": m.end_time.isoformat() if m.end_time else None,
                        "success": m.success,
                        "error_type": m.error_type,
                        "response_time": m.response_time,
                        "results_count": m.results_count,
                        "ip_used": m.ip_used,
                        "user_agent_used": m.user_agent_used
                    }
                    for m in self.query_metrics
                ]
            }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Metrics exported to {filename}")
        except Exception as e:
            print(f"⚠️  Failed to export metrics: {e}")

# Factory function for easy integration
def create_rate_limiter(tor_manager=None, **config_kwargs) -> AdvancedRateLimiter:
    """Create rate limiter with custom configuration"""
    config = RateLimitConfig(**config_kwargs)
    return AdvancedRateLimiter(config, tor_manager)
