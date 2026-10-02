using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using cvoluşturma.Models;

namespace cvoluşturma.Controllers
{
    public class AccountController : Controller
    {
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly SignInManager<ApplicationUser> _signInManager;

        public AccountController(UserManager<ApplicationUser> userManager, SignInManager<ApplicationUser> signInManager)
        {
            _userManager = userManager;
            _signInManager = signInManager;
        }

        [HttpGet]
        public IActionResult Login(string? returnUrl = null)
        {
            if (User.Identity?.IsAuthenticated == true)
                return RedirectToAction("Builder", "Home");
            ViewData["ReturnUrl"] = returnUrl;
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Login(string email, string password, string? returnUrl = null)
        {
            ViewData["ReturnUrl"] = returnUrl;

            if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(password))
            {
                ModelState.AddModelError("", "E-posta ve şifre zorunludur.");
                return View();
            }

            // lockoutOnFailure: true -> 5 denemede hesap kilitlenir
            var result = await _signInManager.PasswordSignInAsync(email, password, isPersistent: true, lockoutOnFailure: true);

            if (result.Succeeded)
            {
                if (!string.IsNullOrEmpty(returnUrl) && Url.IsLocalUrl(returnUrl))
                    return Redirect(returnUrl);
                return RedirectToAction("Builder", "Home");
            }

            if (result.IsLockedOut)
            {
                ModelState.AddModelError("", "Cok fazla basarisiz deneme. Hesabiniz 15 dakika kilitlendi.");
                return View();
            }

            ModelState.AddModelError("", "E-posta veya sifre hatali.");
            return View();
        }

        [HttpGet]
        public IActionResult Register()
        {
            if (User.Identity?.IsAuthenticated == true)
                return RedirectToAction("Builder", "Home");
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Register(string email, string password, string passwordConfirm)
        {
            if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(password))
            {
                ModelState.AddModelError("", "E-posta ve sifre zorunludur.");
                return View();
            }

            if (password != passwordConfirm)
            {
                ModelState.AddModelError("", "Sifreler eslesmıyor.");
                return View();
            }

            if (password.Length < 6)
            {
                ModelState.AddModelError("", "Sifre en az 6 karakter olmalidir.");
                return View();
            }

            var user = new ApplicationUser { UserName = email, Email = email };
            var result = await _userManager.CreateAsync(user, password);

            if (result.Succeeded)
            {
                await _signInManager.SignInAsync(user, isPersistent: true);
                return RedirectToAction("Builder", "Home");
            }

            foreach (var err in result.Errors)
            {
                var msg = err.Code switch
                {
                    "DuplicateEmail" => "Bu e-posta adresi zaten kayitli.",
                    "DuplicateUserName" => "Bu e-posta adresi zaten kullaniliyor.",
                    "InvalidEmail" => "Gecersiz e-posta adresi.",
                    _ => err.Description
                };
                ModelState.AddModelError("", msg);
            }

            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize]
        public async Task<IActionResult> Logout()
        {
            await _signInManager.SignOutAsync();
            return RedirectToAction("Index", "Home");
        }
    }
}
